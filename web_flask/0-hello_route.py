#!/usr/bin/python3
"""
This module Utilizes basic routes and simple
html display
"""
from flask import Flask

# Function that creates the app


def create_app(None):
    """ This is the main function that is called
    when creating a flask app and must be returned
    """
    app = Flask(__name__)

    @app.route('/', strict_slashes=False)
    def hello_world():
        """ Function returns a very basic html string without any tags"""
        return 'Hello HBNB!'
    return app


# Create the App
APP = create_app()
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000, debug=True)
