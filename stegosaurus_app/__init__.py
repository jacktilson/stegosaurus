from flask import Flask, render_template
app = Flask(__name__)


##################
# Core App Pages #
##################

# Define the homepage
@app.route('/')
def home():
    """Renders the temp splash page."""
<<<<<<< HEAD
    return render_template('index.html')
  
  
####################
# HTTP Error Pages #
####################
  
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 


  
# If we run directly, then trigger the WSGI dev server. 
=======
    return render_template('old_index.html')
>>>>>>> 186614e293dd47aacd3c36bd8992ff10c162a9c7
if __name__ == "__main__":
    app.run()