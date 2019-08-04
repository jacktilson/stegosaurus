
################################################################
# This script is triggered by the Apache2 stegapp virtual host #
# in order to launch the flask application and relevant routes #
################################################################


#!/usr/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/flask-app/stegosaurus/")

from steg_server.app import app as application
application.secret_key = 'steggy-key-haha'