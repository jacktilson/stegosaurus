#####################
# Load Dependencies #
#####################

from .app import app
from flask import request, send_file, render_template, jsonify, redirect, url_for, send_from_directory, redirect
from steg_lib.steg import *
from .gen_transaction_id import *
from .core_functions import *
from io import BytesIO
import os, glob, json

###########################
# Shared Encode Functions #
###########################
""" This section defines functions for code required more than
once in the /decode/process, /encode/upload, /encode/space, /encode/complete, 
/encode/download, /encode/delete routes. """

def reply_error_json(resp_msg, http_code=400):
    """Used to return json containing error information and HTTP exception
    in the event that a route encounters a problem."""
    return jsonify({"error_msg": resp_msg}), http_code

def is_json(myjson):
    """Tests whether an object is a JSON."""
    try:
        json_object = json.loads(myjson)
    except:
        return False
    return True
  
def get_temp_path(trans_id, temp_sub_dir, file_suffix, file_exists=True, file_ext=''):
    """Used to return a full file path for a file conformant with
    the temp (upload) directory structure. The file extension (if
    one exits) is sought and automatically added."""
    file_dir_abs = os.path.join(app.root_path, "temp", temp_sub_dir) 
    if not os.path.isdir(file_dir_abs):
      os.makedirs(file_dir_abs) # handle event of directory not existing.
    if file_exists:
      # Change dir to the one with file in it.
      os.chdir(file_dir_abs)
      # Get the the file name of file concerned.
      file_name = f'{trans_id}_{file_suffix}'
      # Find the file extension for the file concerned.
      try: 
        file_loc_abs = os.path.join(file_dir_abs, glob.glob(f'{file_name}*')[0])
      except:
        # If the file does not exist.
        return False, None
    elif not file_exists:
      file_loc_abs = os.path.join(file_dir_abs, f'{trans_id}_{file_suffix}.{file_ext}')
      
    return True, file_loc_abs
  
def read_data_bytes(trans_id):
    """Reads and returns the bytes of a transaction data file."""
    data_file_path = get_temp_path(trans_id, 'data', 'data')[1]
    with open(data_file_path, "rb") as file:
      data_file_bytes = file.read()
    return data_file_bytes
  
def get_img_ext(trans_id):
    """Serves to obtain the file extension, without the dot, of the
    original transaction image file. This is useful as it will also
    be the file extension of the resultant encoded image."""
    file_dir_abs = os.path.join(app.root_path, "temp", "originals")
    # Change dir to the one with file in it.
    os.chdir(file_dir_abs)
    # Get the the file name of file concerned.
    file_name = f'{trans_id}_orig'
    # Find the file extension for the original image..
    file_name_with_ext = glob.glob(f'{file_name}*')[0]
    # Strip the file name part.
    file_ext = file_name_with_ext.replace(f'{file_name}.', '')
    # Return the extension WITH THE DOT.
    return file_ext
    
def store_file_temp(trans_id, file, temp_sub_dir, file_suffix):
    """A general function to store a file in the temp (upload) directory.
    This is utilised by the upload route to save the original image, and
    also the complete route to store the data file."""
    # Set full absolute path of file for transaction.
    file_dir = os.path.join(app.root_path, "temp", temp_sub_dir) 
    if not os.path.isdir(file_dir):
      os.makedirs(file_dir) # handle event of directory not existing.
    # Get file extension
    try:
      disect_name = file.filename.split('.')
    except:
      return None
    ext = f'.{disect_name[len(disect_name)-1]}' # Ext will always be text after final dot.
    # Form absolute path for file to save at.
    file_path = os.path.join(file_dir, f'{trans_id}_{file_suffix}{ext}')
    # Perform the save of file.
    file.save(file_path)
    return file_path
 

def build_flags(str_params, int_params, request):
    """Serves to create a dict for the flags/kwargs of
    space_available and encode functions in steg_lib."""
  
    # Fetch the transaction ID for request in the event of error.
    trans_id = None
    if request.method == "GET":
      trans_id = request.args.get('trans_id', default=None)
    elif request.method == "POST":
      trans_id = request.form.get('trans_id', default=None)

    # Build the dict
    flags_dict = {}
    # Inspect request for all desired params.
    for param in str_params + int_params:
      value = None
      if request.method == "GET":
        value = request.args.get(param, default=None)
      elif request.method == "POST":
        value = request.form.get(param, default=None)
      # If the param was in the request, add to dict as appropriate.
      if value is not None:
        if param in int_params:
          # Test if what we expect to be int can be expressed as an int.
          try:
            flags_dict[param] = int(value)
          # If not, raise error.
          except:
             return reply_error_json(f'There was a problem with the {param} fed to encode function.')
        elif param in str_params:
          # Test if what we expect to be str can be expressed as a str.
          try:
            flags_dict[param] = str(value)
          # If not, raise error.
          except:
            return reply_error_json(f'There was a problem with the {param} fed to encode function.')
    # Once all params have been inspected against request, return the flags dictionary.      
    return flags_dict 
  
def check_trans_id(trans_id, file_type):
    """Used to see if the original / encoded / decoded image is still on
    server for this transaction ID."""
    if trans_id == None:
      return reply_error_json('The transaction ID was not present in the request.')
    
    if file_type == 'original':
      if not get_temp_path(trans_id, 'originals', 'orig')[0]:
        return reply_error_json('The transaction ID is not valid as there is no corresponding original image.')
    elif file_type == 'encoded':
      if not get_temp_path(trans_id, 'encoded', 'encoded')[0]:
        return reply_error_json('The transaction ID is not valid as there is no corresponding encoded image.')
    else:
      return reply_error_json('An error occured when trying to validate the transaction ID.')
      
    return True # All tests must have passed.
  
def check_n_lsb(trans_id, n_lsb):
    """Used to see whether the prospective number of least significant 
    bits is not an int, is less than 1 or is in excess
    of the bitdepth of the image concerned."""
    
    # Define what to do if the proposition is invalid.
    fail_response = reply_error_json('The n_lsb value provided is invalid.')
    try:
      int(n_lsb)
    except:
      return fail_response
    
    # Test suitability of proposed least significant bits.
    img_path = get_temp_path(trans_id, 'originals', 'orig')[1]
    if n_lsb < 1 or n_lsb > get_img_meta(read_img(img_path))[3]:
      return fail_response
    else:
      return True
     
def get_size(start_path, divisor = 1e+6):
    """Recursively returns the size of all directories at the start 
    path and beyond in megabytes by default. Divisors can be applied to
    convert to the desired units. Divisor of 1 will return in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size / divisor # return in desired units, default bytes.
  
def validate_temp(file, dir_max_mb = 10000):
    """Will test whether the proposed file upload would cause
    problems with any storage space ceilings."""
    temp_dir = os.path.join(app.root_path, 'temp')
    temp_dir_size = get_size(temp_dir)
    file_size = get_file_size(file)/1e+6
    if temp_dir_size >= dir_max_mb:
      return reply_error_json('The upload directory is at capacity.')
    elif temp_dir_size + file_size >= dir_max_mb:
      return reply_error_json('The upload directory will exceed capacity if file was to be saved.')
    return True
  
def get_file_size(file):
    """Simply takes a file object and returns its size in bytes."""
    file.seek(0,os.SEEK_END)
    size_bytes = file.tell()
    file.seek(0)
    return size_bytes
      