""" This file contains the flask routes for the main functionality of the app """

from app import app
from flask import request, send_file, render_template
from io import BytesIO

# Define the homepage
@app.route('/')
def home():
    """Renders the temp splash page."""
    return render_template('index.html')
  
# Define the file upload test page
@app.route('/filetest', methods = ['POST'])
def filetest():
  if request.method == 'POST':
    f = request.files['file']
    return send_file(BytesIO(f.read()),
                    attachment_filename = 'file.bmp')
  else:
    return 'no request received'