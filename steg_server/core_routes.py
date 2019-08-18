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
import os, glob, json, requests, base64, boto3, botocore, pickle

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
  
################################################
# Encode Image Transaction ID Generation Route #
#################################################
 
@app.route('/encode/init', methods = ['GET'])
def init_encode():
  
  # Generate a file name / transaction ID.
  trans_id = gen()
  
  # Hand off the ID to client.
  return jsonify({"trans_id": trans_id})
  
###########################################
# Encode Image File Upload Response Route #
###########################################
  
@app.route('/encode/image/upload', methods = ['POST'])
def upload_image_encode():
    
  # Obtain transaction ID from POST request.
  trans_id = request.form.get("trans_id", default=None)
  if trans_id is None: return reply_error_json('Transaction ID was not present in the POST request.')
  
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

###########################################
# Encode Data File Upload Response Route #
###########################################
  
@app.route('/encode/data/upload', methods = ['POST'])
def upload_data_encode():
    
  # Obtain transaction ID from POST request.
  trans_id = request.form.get("trans_id", default=None)
  if trans_id is None: return reply_error_json('Transaction ID was not present in the POST request.')
  
  # Obtain image from POST request.
  data_file = request.files.get('data_file', default=None)
  if data_file is None: return reply_error_json('Data file was not present in the POST request.')
  
  # Test if temp folder has capacity for this.
  storage_test = validate_temp(data_file)
  if storage_test != True: return storage_test
  
  # Drop the image in relevant directory, retain path.
  data_abs_path = store_file_temp(trans_id, data_file, 'data', 'data')
  if data_abs_path is None: reply_error_json('The data file uploaded does not have an extension.')

  # Grab information about the newly saved data file.
  data_size = file_size = get_file_size(data_file)
  
  # Hand off information to client.
  return jsonify({"trans_id": trans_id, "data_bytes": data_size})

############################################################################################
# Asynchronous Space Check Route: How much encodable space with this N_LSB for this image? #
############################################################################################

@app.route('/encode/image/space', methods = ['GET'])
def space_available_encode():
  
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
  
########################################################################################################
# Asynchronous Space Check Route: How much space required in img to accom 1 LSB encoding of data file? #
########################################################################################################

@app.route('/encode/data/space', methods = ['GET'])
def space_required_encode():
  
    """ NOTE: THIS ROUTE IS INCOMPLETE 
    Pending core team to create steg_lib space_required function to be called here."""
  
    # Gather relevant GET request elements
    
    # Obtain and validate transaction ID.
    trans_id = request.args.get('trans_id', default=None)
    trans_id_test = check_trans_id(trans_id, 'original')
    if trans_id_test != True: return trans_id_test
    
    # Obtain filename.
    filename = request.args.get('filename', default=None)
    if filename is None: reply_error_json('The filename was not present in the request.')
      
    # Obtain filename.
    extension = request.args.get('extension', default=None)
    if extension is None: reply_error_json('The file extension was not present in the request.')
    
    # Perform analysis of how many pixels are ideal for the data file's target image.
    num_data_bytes = len(read_file_bytes(trans_id, 'data', 'data'))
    num_fname_bytes = len(filename.encode())
    num_ext_bytes = len(extension.encode())
    space_required = space_required(num_fname_bytes, num_ext_bytes, num_data_bytes)
    
    # Hand back a JSON on success.
    return jsonify({"space_required": space_required})
    
#####################################
# Encoding User Flow Complete Route #
#####################################

@app.route('/encode/complete', methods = ['POST'])
def complete_encode():
    print("********** REQUEST RECEIVED ********* ")
  
    # Seek to relevant POST data, setting as none where not in request.
    
    # Obtain and validate transaction ID
    trans_id = request.form.get('trans_id', default=None)
    trans_id_test = check_trans_id(trans_id, 'original')
    if trans_id_test != True: return trans_id_test
    
    # Validate the proposed number of LSBs.
    n_lsb = int(request.form.get('n_lsb', default=1))
    n_lsb_test = check_n_lsb(trans_id, n_lsb)
    if n_lsb_test != True: return n_lsb_test
    
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

    
    # Read the original image into bytes, and prep for HTTP.
    img_bytes = read_file_bytes(trans_id, 'originals', 'orig')
    img_bytes = base64.encodebytes(img_bytes)
    img_bytes = img_bytes.decode('ascii')
    
    # Read the data file into bytes, and prep for HTTP.
    data_bytes = read_file_bytes(trans_id, 'data', 'data')
    data_bytes = base64.encodebytes(data_bytes)
    data_bytes = data_bytes.decode('ascii')
    
    # Check possible flags against what was actually sent in the request, build flags ready for encode.
    flags_enc = build_flags(['filename', 'extension', 'password'], ['n_lsb'], request)
    
    # Prepare to send to S3.
    s3_json = json.dumps({"function": "encode",
                          "trans_id": trans_id,
                          "img_bytes": img_bytes,
                          "data_bytes": data_bytes,
                          "flags": flags_enc})
    
    # Connect to S3.
    s3 = boto3.resource('s3',
     aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
     aws_secret_access_key=os.environ["AWS_SECRET_KEY"])
      
    # Dump the JSON in S3 bucket so lambda can pick up.
    s3.Bucket(os.environ["AWS_BUCKET"]).put_object(Key=f'encode/recipe/{trans_id}.json', Body=s3_json)
    
    # Provide recipe for lambda, ie transaction ID so it can find the files in S3 bucket.
    lambda_json = json.dumps({"function": "encode",
                              "trans_id": trans_id})
    
    # Alert lambda of new work.
    lambda_headers = {"Content-Type": "application/json"}
    lambda_api_url = 'https://bhczbacdz5.execute-api.eu-west-2.amazonaws.com/deploy/steg-encode'
    print("*** INIT API CALL TO LAMBDA ***")
    print(lambda_api_url)
    response = requests.post(lambda_api_url, headers=lambda_headers, data=lambda_json)
    print("*** COMPLETED API CALL TO LAMBDA ***")
    print(response)
    #print(response.json)
    #print(response.text)
    
    # Handle response.
    lambda_result = json.loads(response.text)
    s3_result_key = lambda_result.get("s3_result_key")
    
    # Fetch encoded data from lambda-linked s3.
    enc_nparray_object = s3.Object('steg-compute-data', s3_result_key)
    enc_nparray_bytes = enc_nparray_object.get()['Body'].read()
    
    # Prepare encoded data for writing to disk.
    enc_nparray = pickle.loads(enc_nparray_bytes)
  
    # Store the result
    write_img(enc_img_path, enc_nparray)
    
    print("*** REQUEST FILLED ***")

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
  
    # Create an arbitrary ID for the JSON to be held in S3.
    trans_id = gen()
    
    # Obtain image and password from POST request.
    img_file = request.files.get('img_file', default=None)
    if img_file is None: return reply_error_json('An image was not present in the POST request.')
    password = request.form.get('password', default=None)
    
    # Load bytes from image, prepare for HTTP.
    img_bytes = img_file.read()
    img_bytes = base64.encodebytes(img_bytes)
    img_bytes = img_bytes.decode('ascii')
    
    # Connect to S3.
    s3 = boto3.resource('s3',
     aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
     aws_secret_access_key=os.environ["AWS_SECRET_KEY"])
    
    # Prepare to send to S3.
    s3_json_dict = {"function": "decode",
                    "img_bytes": img_bytes}
    
    # Append password if one given.
    if password is not None: s3_json_dict["password"] = password
      
    # Pack into JSON for S3.
    s3_json = json.dumps(s3_json_dict)
      
    # Dump the JSON in S3 bucket so lambda can pick up.
    s3.Bucket(os.environ["AWS_BUCKET"]).put_object(Key=f'decode/recipe/{trans_id}.json', Body=s3_json)
   
    # Prepare recipe to send to lambda.
    lambda_json = json.dumps({"function": "decode",
                              "trans_id": trans_id})
    
    # POST data to lambda for computation.
    headers = {"Content-Type": "application/json"}
    lambda_api_url = 'https://0vxfryzq1b.execute-api.eu-west-2.amazonaws.com/deploy/steg-decode'
    print("**** START DECODE API CALL ****")
    print(lambda_api_url)
    response = requests.post(lambda_api_url, headers=headers, data=lambda_json)
    print("**** END DECODE API CALL ****")
    print(str(response.json))
    print(response.text)
    
    # Handle response.
    lambda_result = json.loads(response.text)
    s3_result_key = lambda_result.get("s3_result_key")
    
    # Fetch lambda payload from S3.
    decode_json_object = s3.Object('steg-compute-data', s3_result_key)
    decode_json_bytes = decode_json_object.get()['Body'].read()
    decode_json = json.loads(decode_json_bytes)
    
    # Unravel data file bytes from JSON.
    data_bytes = decode_json.get("data_bytes")
    data_bytes = data_bytes.encode('ascii')
    data_bytes = base64.decodebytes(data_bytes)
    
    # Get the filename for data file.
    attachment_filename = decode_json.get("file_name")
    
    # Send back the decoded output file.
    return send_file(BytesIO(data_bytes), attachment_filename=attachment_filename, as_attachment=True)
