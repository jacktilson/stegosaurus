"""  This file triggers the Flask instance, and loads all of the routes types. """

#########################
# Create Flask Instance #
#########################

import os
from flask import Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'temp')
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 # Max post request size 64MB
app.config['CUSTOM_STATIC_PATH'] = os.path.join(app.root_path, 'temp')
app.config['APP_HOST'] = "stegosaurus.online"

#############################
# Load Core App Page Routes #
#############################

from .core_routes import *  

##########################
# HTTP Error Page Routes #
##########################

from .error_routes import *

#######################
# Direct Run Handling #
#######################
if __name__ == "__main__":
    app.run()