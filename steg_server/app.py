"""  This file triggers the Flask instance, and loads all of the routes types. """

#########################
# Create Flask Instance #
#########################

import os
from flask import Flask
app = Flask(__name__, static_url_path="/")
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'temp')
app.config['CUSTOM_STATIC_PATH'] = os.path.join(app.root_path, 'temp')
app.config['APP_HOST'] = "stegosaurus.online"

#print(f"APP_ROOT VARIABLE VALUE::::: {app_root}")
#print(f"app.root_path VARIABLE VALUE::::: {app.root_path}")
#print(f"app.instance_path VARIABLE VALUE::::: {app.instance_path}")
#print("*********************************")

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