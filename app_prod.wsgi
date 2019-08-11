
################################################################
# This script is triggered by the Apache2 stegapp virtual host #
# in order to launch the flask application and relevant routes #
################################################################

###########################################
# DO NOT ADD THIS TO ANY GIT REPOSITORIES #
###########################################


#!/usr/bin/python3.6
import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/flask-app/stegosaurus/")

from steg_server.app import app as application
application.secret_key = 'steggy-key-haha'
os.environ["AWS_ACCESS_KEY"] = 'AKIAZEOA22S2WRPHY43Q'
os.environ["AWS_SECRET_KEY"] = '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'
os.environ["AWS_BUCKET"] = 'steg-compute-data'