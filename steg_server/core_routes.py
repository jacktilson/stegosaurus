""" This file contains the flask routes for the main functionality of the app """

#####################
# Load Dependencies #
#####################

from .app import app, app_root
from flask import request, send_file, render_template, jsonify, redirect, url_for, send_from_directory, redirect
from steg_lib.steg import *
from .gen_transaction_id import *
from io import BytesIO
import os, glob

##################
# Homepage Route #
##################

@app.route('/')
def home():
    """Renders the temp splash page."""
    # Ensure domain in use is kosher.
    if request.host == app.config['APP_HOST']: 
      return send_from_directory(app.static_folder, 'index.html')
    else:
      return send_from_directory(app.static_folder, 'bad_domain.html')



##########################
# File Upload Test Route #
##########################

@app.route('/filetest', methods = ['POST'])
def filetest():
  if request.method == 'POST':
    f = request.files['file']
    return send_file(BytesIO(f.read()),
                    attachment_filename = 'file.bmp')
  else:
    return 'no request received'
  
  
#######################################
# Temp/Upload Files HTTP Access Route #
#######################################

@app.route('/temp/<path:filename>')
def temp_access(filename):
    return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename, conditional=True)
  
###########################
# Shared Encode Functions #
###########################
""" This section defines functions for code required more than
once in the /encode, /space or /complete routes. """

def reply_error_json(trans_id, resp_code, resp_msg):
    """Used to return json containing error information
    in the event that a route encounters a problem."""
    return(jsonify({"trans_id": trans_id,
                    "resp_code": resp_code,
                    "resp_msg": resp_msg}))
  
def form_temp_file_path(trans_id, temp_sub_dir, file_suffix, file_exists=True, file_ext=''):
    """Used to return a full file path for a file conformant with
    the temp (upload) directory structure. The file extension (if
    one exits) is sought and automatically added."""
    file_dir_abs = os.path.join(app_root, "temp", temp_sub_dir) 
    if not os.path.isdir(file_dir_abs):
      os.makedirs(file_dir_abs) # handle event of directory not existing.
    if file_exists:
      # Change dir to the one with file in it.
      os.chdir(file_dir_abs)
      # Get the the file name of file concerned.
      file_name = f'{trans_id}_{file_suffix}'
      # Find the file extension for the original image..
      print(glob.glob("*"))
      print(glob.glob(f'{file_name}*'))
      print(glob.glob(f'{file_name}'))
      file_loc_abs = os.path.join(file_dir_abs, glob.glob(f'{file_name}*')[0])
    
    elif not file_exists:
      file_loc_abs = os.path.join(file_dir_abs, f'{trans_id}_{file_suffix}{file_ext}')
      
    return file_loc_abs
  
def form_orig_img_path(trans_id):
    """Used to produce the path to the originally uploaded image
    based on the current transaction ID."""
    return form_temp_file_path(trans_id, 'originals', 'orig')
  
def form_data_file_path(trans_id):
    """Used to produce the path to the uploaded data file
    based on the current transaction ID."""
    return form_temp_file_path(trans_id, 'data', 'data')
  
def read_data_file_bytes(trans_id):
    data_file_path = form_data_file_path(trans_id)
    with open(data_file_path, "rb") as file:
      data_file_bytes = file.read()
    return data_file_bytes
  
def form_enc_file_path(trans_id, file_exits=True, file_ext=''):
    """Used to produce the path to the resultant encoded image
    based on the current transaction ID."""
    return form_temp_file_path(trans_id, 'encoded', 'encoded', file_exits, file_ext)
  
def get_img_ext(trans_id):
    """Serves to obtain the file extension, with the dot, of the
    original transaction image file. This is useful as it will also
    be the file extension of the resultant encoded image."""
    file_dir_abs = os.path.join(app_root, "temp", "originals")
    # Change dir to the one with file in it.
    os.chdir(file_dir_abs)
    # Get the the file name of file concerned.
    file_name = f'{trans_id}_orig'
    # Find the file extension for the original image..
    file_name_with_ext = glob.glob(f'{file_name}*')[0]
    # Strip the file name part.
    file_ext = file_name_with_ext.replace(f'{file_name}', '')
    # Return the extension WITH THE DOT.
    return file_ext
    
def store_file_temp(trans_id, file, temp_sub_dir, file_suffix):
    """A general function to store a file in the temp (upload) directory.
    This is utilised by the upload route to save the original image, and
    also the complete route to store the data file."""
    # Set full absolute path of file for transaction.
    file_dir_abs = os.path.join(app_root, "temp", temp_sub_dir) 
    if not os.path.isdir(file_dir_abs):
      os.makedirs(file_dir_abs) # handle event of directory not existing.
    # Get file extension
    ext = '.' + file.filename[-3:].lower() # N E E D S  I M P R O V E M E N T
    # Form absolute path for file to save at.
    file_loc_abs = os.path.join(file_dir_abs, f'{trans_id}_{file_suffix}{ext}')
    # Perform the save of file.
    file.save(file_loc_abs)
    return file_loc_abs
  
def build_flags(list_get_params, this_request):
    """Serves to create a dict for the flags/kwargs of
    space_available and encode functions in steg_lib."""
    steg_lib_flags = {}
    if this_request.method == 'GET':
      for param in list_get_params:
        param_val = this_request.args.get(param, default=None)
        if param_val != None:
          # See if it's an integer.
          try:
            steg_lib_flags[param] = int(param_val)
          # If not, just store it as its original form e.g. string.
          except:
            steg_lib_flags[param] = param_val
    elif this_request.method == 'POST':
        for param in list_get_params:
          param_val = this_request.form.get(param, default=None)
        if param_val != None:
          steg_lib_flags[param] = param_val
    return steg_lib_flags
  
def check_trans_id(trans_id):
    """Used to see if the original image is still on
    server for this transaction ID."""
    if trans_id == None:
      return reply_error_json(trans_id, 1, 'The transaction ID was not present in the request.')
    if not os.path.isfile(form_orig_img_path(trans_id)):
      return reply_error_json(trans_id, 2, 'The transaction ID is not valid as there is no corresponding image.')
    else:
      return True
  
def check_n_lsb(trans_id, n_lsb):
    """Used to see whether the prospective number of least significant 
    bits is not an int, is less than 1 or is in excess
    of the bitdepth of the image concerned."""
    fail_response = reply_error_json(trans_id, 3, 'The n_lsb value provided is invalid.')
    try:
      int(n_lsb)
    except:
      return fail_response
    print("THE PATH TO IMG**************")
    print(form_orig_img_path(trans_id))
    if n_lsb < 1 or n_lsb > get_img_meta(read_img(form_orig_img_path(trans_id)))[3]:
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
  
def validate_temp_dir(data_file, dir_max_mb = 10000):
    """Will test whether the proposed file upload would cause
    problems with any storage space ceilings."""
    temp_dir = os.path.join(app_root, 'temp')
    temp_dir_size = get_size(temp_dir)
    if temp_dir_size >= dir_max_mb:
      return reply_error_json(trans_id, 5, 'The upload directory is at capacity.')
    elif temp_dir_size + (len(data_file.read())/1e+6) >= dir_max_mb:
      return reply_error_json(trans_id, 6, 'The upload directory will exceed capacity if file was to be saved.')
    return True
      
######################################
# Encode Image Upload Response Route #
######################################
  
@app.route('/encode/upload', methods = ['POST'])
def upload_encode():
    
  # Generate a file name / transaction ID.
  trans_id = gen()
  
  # Obtain image from POST request.
  img = request.files['imgFile']
  
  # Drop the image in relevant directory, retain path.
  img_abs_path = store_file_temp(trans_id, img, 'originals', 'orig')

  # Grab information about the newly saved image.
  img_meta = get_img_meta(read_img(img_abs_path))
  
  # Hand off information to client.
  return jsonify({"trans_id": trans_id, "width": img_meta[0],
                  "height": img_meta[1], "channels": img_meta[2],
                  "bitdepth": img_meta[3]})

##################################
# Asynchronous Space Check Route #
##################################

@app.route('/encode/space', methods = ['GET'])
def space_encode():
  
    # Gather relevant GET request elements
    trans_id = request.args.get('trans_id', default=None)
    n_lsb = int(request.args.get('n_lsb', default=1))
    
    # Perform error catching.
    trans_id_test = check_trans_id(trans_id)
    if trans_id_test != True: return trans_id_test
    n_lsb_test = check_n_lsb(trans_id, n_lsb)
    if n_lsb_test != True: return n_lsb_test
    
    # Perform space analysis.
    list_get_params = ['n_lsb', 'extension', 'filename']
    flags_sa = build_flags(list_get_params, request)
    print(flags_sa)
    print(form_orig_img_path(trans_id))
    space = space_available(read_img(form_orig_img_path(trans_id)), **flags_sa)
    
    # Hand back a JSON on success.
    return jsonify({"trans_id": trans_id, "space_available": space})
    
#####################################
# Encoding User Flow Complete Route #
#####################################

@app.route('/encode/complete', methods = ['POST'])
def complete_encode():
  
    def json_reply(trans_id, resp_code, resp_msg):
      pre_json_space = {"trans_id": trans_id,
                       "err_code": err_code,
                       "resp_msg": resp_msg}
      return jsonify(pre_json_complete)
   
  
    # Seek to relevant POST data, setting as none where not in request.
    trans_id = request.form.get('trans_id', default=None)
    n_lsb = int(request.form.get('n_lsb', default=None))
    try:
        data_file = request.files['data_file']
    except:
        data_file = None
        
        
    # Check if transaction ID is there.
    trans_id_test = check_trans_id(trans_id)
    if trans_id_test != True: return trans_id_test
    
    # Scrutinise suitability of LSB for image.
    n_lsb_test = check_n_lsb(trans_id, n_lsb)
    if n_lsb_test != True: return n_lsb_test
    
    # Check whether the data file was in the request.
    if data_file == None: return reply_error_json(trans_id, 4, 'The data file was not received.')

    # Check whether temp dir can handle this.
    temp_dir_cap_test = validate_temp_dir(data_file)
    if temp_dir_cap_test != True: return temp_dir_cap_test
    
    # Store the data file.
    store_file_temp(trans_id, data_file, 'data', 'data')
    
    # Set the prospective destination file with extension.
    enc_file_path = form_enc_file_path(trans_id, file_exits=False, file_ext=get_img_ext(trans_id))

    # Process the encoding, feeding original image path, data file path and flags to encode function.
    list_get_params = ['n_lsb', 'extension', 'filename']
    flags_enc = build_flags(list_get_params, request)
    write_img(enc_file_path, encode(read_img(form_orig_img_path(trans_id)), read_data_file_bytes(trans_id), **flags_enc))
    
    # Hand off the result.  
    return jsonify({"trans_id": trans_id, "resp_code": 0,
                    "resp_msg": 'Data encoded to image successfully.'})
      
    
