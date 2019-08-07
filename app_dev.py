from steg_server.app import app
if __name__ == "__main__":
    app.config['APP_HOST'] = "localhost:5000"
    app.run()