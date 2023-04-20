from flask import Flask

# Function that creates the app
def create_app(test_config=None):
    app = Flask(__name__)
    @app.route('/', strict_slashes=False)
    def hello_world():
        return 'Hello HBNB!'
    return app

# Create the App
APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)
