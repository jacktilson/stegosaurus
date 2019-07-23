"""  This file triggers the Flask instance, and loads all of the routes types. """

#########################
# Create Flask Instance #
#########################

from flask import Flask
app = Flask(__name__)

#############################
# Load Core App Page Routes #
#############################

from core_routes import *  

##########################
# HTTP Error Page Routes #
##########################

from error_routes import *

#######################
# Direct Run Handling #
#######################
if __name__ == "__main__":
    app.run()