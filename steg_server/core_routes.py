""" This file contains the flask routes for the main functionality of the app """

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

##################
# Homepage Route #
##################

@app.route('/')
def home():
    """Renders the temp splash page."""
    # Ensure domain in use is kosher.
    if request.host == app.config['APP_HOST']: 
      return send_from_directory(os.path.join(app.static_folder, "client"), 'index.html')
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
  
      
######################################
# Encode Image Upload Response Route #
######################################
  
@app.route('/encode/upload', methods = ['POST'])
def upload_encode():
    
  # Generate a file name / transaction ID.
  trans_id = gen()
  
  # Obtain image from POST request.
  img_file = request.files.get('img_file', default=None)
  if img_file is None: return reply_error_json(trans_id, 'Original image was not present in the POST request.')
  
  # Test if temp folder has capacity for this.
  temp_dir_cap_test = validate_temp_dir(img_file)
  if temp_dir_cap_test != True: return temp_dir_cap_test
  
  # Drop the image in relevant directory, retain path.
  img_abs_path = store_file_temp(trans_id, img_file, 'originals', 'orig')
  if img_abs_path is None: reply_error_json(trans_id, 'The image file uploaded does not have an extension.')

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
    
    # Obtain and validate transaction ID.
    trans_id = request.args.get('trans_id', default=None)
    trans_id_test = check_trans_id(trans_id, 'original')
    if trans_id_test != True: return trans_id_test
    
    # Obtain and validate proposed LSBs.
    n_lsb = int(request.args.get('n_lsb', default=1))
    n_lsb_test = check_n_lsb(trans_id, n_lsb)
    if n_lsb_test != True: return n_lsb_test
    
    # Perform space analysis.
    flags_sa = build_flags(['filename', 'extension'], ['n_lsb'], request)
    space = space_available(read_img(form_orig_img_path(trans_id)[1]), **flags_sa)
    
    # Hand back a JSON on success.
    return jsonify({"trans_id": trans_id, "resp_code": 0, 
                    "space_available": space})
    
#####################################
# Encoding User Flow Complete Route #
#####################################

@app.route('/encode/complete', methods = ['POST'])
def complete_encode():
  
    # Seek to relevant POST data, setting as none where not in request.
    
    # Obtain and validate transaction ID
    trans_id = request.form.get('trans_id', default=None)
    trans_id_test = check_trans_id(trans_id, 'original')
    if trans_id_test != True: return trans_id_test
    
    # Obtain and validate the proposed number of LSBs.
    n_lsb = int(request.form.get('n_lsb', default=None))
    n_lsb_test = check_n_lsb(trans_id, n_lsb)
    if n_lsb_test != True: return n_lsb_test
    
    # Obtain and validate the data file.
    data_file = request.files.get('data_file', default=None)
    if data_file is None: return reply_error_json(trans_id, 'The data file was not received.')

    # Check whether temp dir can handle this data file.
    temp_dir_cap_test = validate_temp_dir(data_file)
    if temp_dir_cap_test != True: return temp_dir_cap_test
    
    # Store the data file.
    data_file_path = store_file_temp(trans_id, data_file, 'data', 'data')
    
    # Set the prospective destination file with extension.
    enc_file_path = form_enc_img_path(trans_id, file_exits=False, file_ext=get_img_ext(trans_id))[1]

    # Read the original image into bytes.
    in_img = read_img(form_orig_img_path(trans_id)[1])
    
    # Read the data file into bytes.
    in_data = read_data_file_bytes(trans_id)
    
    # Process the encoding, feeding original image path, data file path and flags to encode function.
    flags_enc = build_flags(['filename', 'extension'], ['n_lsb'], request)
    
    # Perform the encoding.
    encoded_img = encode(in_img, in_data, **flags_enc)
    
    # Store the result
    write_img(enc_file_path, encoded_img)

    # Hand off the result.  
    return jsonify({"trans_id": trans_id, "resp_code": 0,
                    "resp_msg": 'Data encoded to image successfully.'})    

#####################################
# Encoded File URL Generation Route #
#####################################

@app.route('/encode/download', methods = ['GET'])
def download_encode():
    
    # Obtain the relevant GET args.
    
    # Obtain and validate transaction ID
    trans_id = request.args.get('trans_id', default=None)
    trans_id_test = check_trans_id(trans_id, 'encoded')
    if trans_id_test != True: return trans_id_test
    
    # Obtain the path for the encoded image.
    enc_img_path_abs = form_enc_img_path(trans_id)[1]
    
    # Obtain the filename with extension.
    enc_img_path_parts = enc_img_path_abs.split(os.sep)
    enc_img_filename = enc_img_path_parts[len(enc_img_path_parts)-1]
    # Now obtain the file extension, taking the text after the last dot.
    enc_img_filename_parts = enc_img_filename.split('.')
    enc_img_ext = enc_img_filename_parts[len(enc_img_filename_parts)-1]
    
    return_filename = f'output.{enc_img_ext}'
    
    # Send off the encoded file
    return send_file(enc_img_path_abs, attachment_filename=return_filename, as_attachment=True)
 
###############################
# Encode Files Deletion Route #
###############################

@app.route('/encode/delete', methods = ['GET'])
def delete_encode():
    
    # Obtain the relevant GET args.
    
    # Obtain and validate transaction ID
    trans_id = request.form.get('trans_id', default=None)
    trans_id_test = check_trans_id(trans_id, 'encoded')
    if trans_id_test != True: return trans_id_test
    
    # Obtain the path for the encoded image.
    orig_img_path_abs = form_orig_img_path(trans_id)[1]
    data_file_path_abs = form_data_file_path(trans_id)[1]
    enc_img_path_abs = form_enc_img_path(trans_id)[1]
    
    # Cycle though files to see if need to delete. Assuming if not found, can ignore.
    if orig_img_path_abs is not None: os.remove(orig_img_path_abs)
    if data_file_path_abs is not None: os.remove(data_file_path_abs)
    if enc_img_path_abs is not None: os.remove(enc_img_path_abs)
      
    return jsonify({"trans_id": trans_id, "resp_code": 0,
                    "resp_msg": 'All encode transaction files deleted successfully.'})
  
  
##############################
# Decode File Upload Process #
##############################

@app.route('/decode/process', methods = ['POST'])
def process_decode():
    
    # Obtain image from POST request.
    dec_img_file = request.files.get('img_file', default=None)
    if dec_img_file is None: return reply_error_json('none', 'An image was not present in the POST request.')
    
    # Perform the decode.
    bytes_file = dec_img_file.read()
    data, meta = decode_img(read_img_binary(bytes_file))
    
    # Fetch metadata
    filename = meta.get("filename")
    extension = meta.get("extension")
    
    # Form attachement filename.
    return_filename = ''
    if filename is None and extension is None:
      return_filename = 'output'
    elif filename is None and extension is not None:
      return_filename = f'output.{extension}'
    elif filename is not None and extension is None:
      return_filename = filename
    elif filename is not None and extension is not None:
      return_filename = f'{filename}.{extension}'
    
    # Send back the decoded output file.
    return send_file(BytesIO(data), attachment_filename=return_filename, as_attachment=True)
    
