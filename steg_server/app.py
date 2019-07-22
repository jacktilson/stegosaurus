"""  This file triggers the Flask instance, and loads all of the routes types. """

from flask import Flask
app = Flask(__name__)

##################
# Core App Pages #
##################

from core_routes import *  

####################
# HTTP Error Pages #
####################

from error_routes import *

#######################
# Direct Run Handling #
#######################
if __name__ == "__main__":
    app.run()