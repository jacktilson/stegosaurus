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
  
      
######################################
# Encode Image Upload Response Route #
######################################
  
@app.route('/encode/upload', methods = ['POST'])
def upload_encode():
    
  # Generate a file name / transaction ID.
  trans_id = gen()
  
  # Obtain image from POST request.
  img_file = request.files.get('img_file', default=None)
  if img_file is None: return reply_error_json('Original image was not present in the POST request.')
  
  # Test if temp folder has capacity for this.
  storage_test = validate_temp(img_file)
  if storage_test != True: return storage_test
  
  # Drop the image in relevant directory, retain path.
  img_abs_path = store_file_temp(trans_id, img_file, 'originals', 'orig')
  if img_abs_path is None: reply_error_json('The image file uploaded does not have an extension.')

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
    img_path = get_temp_path(trans_id, 'originals', 'orig')[1]
    flags_sa = build_flags(['filename', 'extension'], ['n_lsb'], request)
    space = space_available(read_img(img_path), **flags_sa)
    
    # Hand back a JSON on success.
    return jsonify({"space_available": space})
    
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
    n_lsb = int(request.form.get('n_lsb', default=1))
    n_lsb_test = check_n_lsb(trans_id, n_lsb)
    if n_lsb_test != True: return n_lsb_test
    
    # Obtain and validate the data file.
    data_file = request.files.get('data_file', default=None)
    if data_file is None: return reply_error_json('The data file was not received.')

    # Check whether temp dir can handle this data file.
    storage_test = validate_temp(data_file)
    if storage_test != True: return storage_test
    
    # Store the data file and retain its path.
    data_file_path = store_file_temp(trans_id, data_file, 'data', 'data')
    
    
    # Define the lossless and lossy file formats.
    retainable_ext = ["bmp", "png", "dib"]
    non_retainable_ext = ["jpeg", "jpg", "jpe", "jp2", "webp", "pbm", "pgm", "ppm", "sr", "ras", "tiff", "tif"]
    # Check if we need to force png (popular and lossless, encoded data not lost), get destination file with extension.
    original_ext = get_img_ext(trans_id, 'originals', 'orig')
    enc_img_path = ''
    if original_ext in retainable_ext:
      enc_img_path = get_temp_path(trans_id, 'encoded', 'encoded', file_exists=False, file_ext=original_ext)[1]
    elif original_ext in non_retainable_ext:
      enc_img_path = get_temp_path(trans_id, 'encoded', 'encoded', file_exists=False, file_ext='png')[1]
    else:
      return reply_error_json('This output image format is not supported.')

    
    # Read the original image into bytes.
    orig_img_path = get_temp_path(trans_id, 'originals', 'orig')[1]
    in_img = read_img(orig_img_path)
    
    # Read the data file into bytes.
    in_data = read_data_bytes(trans_id)
    
    # Process the encoding, feeding original image path, data file path and flags to encode function.
    flags_enc = build_flags(['filename', 'extension'], ['n_lsb'], request)
    
    # Perform the encoding.
    encoded_img = encode(in_img, in_data, **flags_enc)
    
    # Store the result
    write_img(enc_img_path, encoded_img)

    # Hand off the result.  
    return jsonify({"resp_msg": 'Data encoded to image successfully.'})    

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
    img_path = get_temp_path(trans_id, 'encoded', 'encoded')[1]
    
    # Obtain the file extension
    img_ext = get_img_ext(trans_id, 'encoded', 'encoded')
    
    # Form the filename of the response image.
    return_filename = f'output.{img_ext}'
    
    # Send off the encoded file
    return send_file(img_path, attachment_filename=return_filename, as_attachment=True)
 
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
    
    # Obtain the paths for the transaction files.
    orig_img_path = get_temp_path(trans_id, 'originals', 'orig')[1]
    data_file_path = get_temp_path(trans_id, 'data', 'data')[1]
    enc_img_path = get_temp_path(trans_id, 'encoded', 'encoded')[1]
    
    # Cycle though files to see if need to delete. Assuming if not found, can ignore.
    if orig_img_path is not None: os.remove(orig_img_path)
    if data_file_path is not None: os.remove(data_file_path)
    if enc_img_path is not None: os.remove(enc_img_path)
      
    return jsonify({"resp_msg": 'All encode transaction files deleted successfully.'})
  
  
##############################
# Decode File Upload Process #
##############################

@app.route('/decode/process', methods = ['POST'])
def process_decode():
    
    # Obtain image from POST request.
    img_file = request.files.get('img_file', default=None)
    if img_file is None: return reply_error_json('An image was not present in the POST request.')
    
    # Perform the decode.
    data, meta = decode_img(read_img_binary(img_file.read()))
    
    # Fetch metadata
    filename = meta.get("filename", "output") #defaults to "output" if "filename" not present 
    extension = meta.get("extension", "") #defaults to "" if "extension" not present
    print("************************")
    print(extension)
    
    # Form attachement filename.
    attachment_filename = f"{filename}.{extension}" if extension != "" else filename
    
    # Send back the decoded output file.
    return send_file(BytesIO(data), attachment_filename=attachment_filename, as_attachment=True)
