#!/usr/bin/python3
"""
This module Utilizes basic routes and simple
html display
"""
from flask import Flask, escape
import os
os.environ["FLASK_APP"] = "2-c_route.py"

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


@app.route('/c/<text>', strict_slashes=False)
def c_func(text):
    """ Function returns a very basic html string and displays parameter
    values and substitutes underscores with an empty space.
    """
    text = text.split('_')
    text = " ".join(text)
    return 'C %s' % escape(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_func(text="is cool"):
    """ Function returns a very basic html string and displays parameter
    values and substitutes underscores with an empty space.
    Also supports default parameter arguments
    """
    text = text.split('_')
    text = " ".join(text)
    return 'Python %s' % escape(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
