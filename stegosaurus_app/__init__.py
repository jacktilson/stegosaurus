from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def home():
    """Renders the temp splash page."""
    return render_template('old_index.html')
if __name__ == "__main__":
    app.run()