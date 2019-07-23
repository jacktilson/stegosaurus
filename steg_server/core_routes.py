""" This file contains the flask routes for the main functionality of the app """

#####################
# Load Dependencies #
#####################

from app import app
from flask import request, send_file, render_template
from io import BytesIO

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