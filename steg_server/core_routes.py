""" This file contains the flask routes for the main functionality of the app """

#####################
# Load Dependencies #
#####################

from .app import app, app_root
from flask import request, send_file, render_template, jsonify, redirect, url_for, send_from_directory
from .steg_lib_deploy import *
from .gen_transaction_id import *
from io import BytesIO
import os

##################
# Homepage Route #
##################

@app.route('/')
def home():
    """Renders the temp splash page."""
    return render_template('index.html')
  
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
    
  # Set name of HTML form attribute containing image.
  img_field_name = 'imgFile'
  # Set path to save image on system.
  img_save_path = 'temp/originals'
  # Obtain image from POST request.
  img = request.files[img_field_name]
  # Get the file extension (last 3 chars of filename).
  ext = '.' + img.filename[-3:].lower()
  # Generate a file name / transaction ID.
  trans_id = gen()

  # Ascertian temp folder to park image inside of.
  target = os.path.join(app_root, img_save_path)
  # Handle event of target not existing. 
  if not os.path.isdir(target):
    os.mkdir(target)
  # Create destination for file.
  dest = '/'.join([target, trans_id + '_orig'])
  # Perform the save.
  img.save(dest)

  # Grab information about the newly saved image.
  img_meta = get_img_meta(read_img(dest))

  # Pack into dictionary.
  pre_json = {"trans_id": trans_id,
              "width": img_meta[0],
              "height": img_meta[1],
              "channels": img_meta[2],
              "bitdepth": img_meta[3]}

  # Hand back as JSON
  return jsonify(pre_json)

##################################
# Asynchronous Space Check Route #
##################################

@app.route('/encode/space', methods = ['GET'])
def space_encode():
  
    def pack_pre_json(trans_id, space_available, err_code):
      pre_json_space = {"trans_id": trans_id,
                       "space_available": space_available,
                       "err_code": err_code}
      return pre_json_space
    
    # Gather request elements
    trans_id = request.args.get('transID') if 'transID' in request.args else 'null'
    n_lsb = int(request.args.get('nBits')) if 'nBits' in request.args else 1
    file_ext = request.args.get('ext') if 'ext' in request.args else 'null'
    file_name = request.args.get('filename') if 'filename' in request.args else 'null'
    
    # Get full absolute path of image for transaction.
    orig_img_dir_rel = 'temp/originals'
    orig_img_dir_abs = os.path.join(app_root, orig_img_dir_rel)
    orig_img_loc_abs = '/'.join([orig_img_dir_abs, trans_id + '_orig'])
    
    # Perform error catching.
    print("PATH INSPECTED")
    print(orig_img_loc_abs)
    err_code = 0
    if not os.path.isfile(orig_img_loc_abs): err_code = 1 # Check if original img exists.
    if n_lsb < 1 or n_lsb > get_img_meta(read_img(orig_img_loc_abs))[3]: err_code = 2 # Check bitdeth of img.
    if err_code != 0: return jsonify(pack_pre_json(trans_id, 'none', err_code))
    
    # Perform space analysis.
    flags_sa = {"n_lsb": n_lsb, "filename": file_name, "extension": file_ext}
    space = space_available(read_img(orig_img_loc_abs), **flags_sa)
    
    # Hand back a JSON.
    return jsonify(pack_pre_json(trans_id, space, err_code))
    
    