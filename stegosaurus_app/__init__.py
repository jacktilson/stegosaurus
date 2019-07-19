from flask import Flask, render_template
from error_code_info import error_info
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

@app.errorhandler(Exception)
def http_error(error):
  
    # Define generic description for error
    gen_err_desc = "We don't quite know what happened here."
    
    # Acquire an explanation of the error code from error_code_info file, less the code itself.
    if error.code in error_info:
    
      # If found, set specific description.
      err_desc = error_info[error.code][4:]
      
      # Declare whether we know about the error.
      err_code_known = True
    
    else:
      
      # If it is not found, set a generic one.
      err_desc = gen_err_desc
      
      # Declare whether we know about the error.
      err_code_known = False
    
    # Render the error page.
    return render_template('http_error.html', err_code = error.code, err_desc = err_desc, err_code_known = err_code_known), error.code

  
# If we run directly, then trigger the WSGI dev server. 
if __name__ == "__main__":
    app.run()