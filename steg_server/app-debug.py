"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def home():
    """Renders the temp splash page."""
    return render_template('old_index.html')


if __name__ == '__main__':
    app.run("0.0.0.0", port=443, ssl_context='adhoc')
