#!/usr/bin/python3
"""
This module Utilizes basic routes and simple
html display
"""
from flask import Flask
import os
os.environ["FLASK_APP"] = "1-hbnb_route.py"

# Function that creates the app


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_school():
    """ Function returns a very basic html string without any tags"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def school():
    """ Function returns a very basic html string without any tags"""
    return 'HBNB'

    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
