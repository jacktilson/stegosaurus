from flask import Flask, render_template
app = Flask(__name__)


##################
# Core App Pages #
##################

# Define the homepage
@app.route('/')
def home():
    """Renders the temp splash page."""
    return render_template('index.html')
  
  
####################
# HTTP Error Pages #
####################
  
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 


  
# If we run directly, then trigger the WSGI dev server. 
if __name__ == "__main__":
    app.run()