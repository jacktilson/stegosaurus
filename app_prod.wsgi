#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/flask-app/stegosaurus/")

from stegosaurus_app import app as application
application.secret_key = 'steggy-key-haha'