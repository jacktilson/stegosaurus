#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/flask-app/stegosaurus/")

from steg_server import app
app.secret_key = 'steggy-key-haha'