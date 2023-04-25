#!/usr/bin/python3
"""
This module Utilizes basic routes and simple
html display and utilizes render_template
which allows rendering of external reference html
files
"""
from flask import Flask, escape, render_template
import os
from models import storage
from models.state import State
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

os.environ["FLASK_APP"] = "7-states_list.py"

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    """ Display Listing of all States:
    """
    if STORAGE_TYPE == "db":
        states = storage.all('State')
    else:
        states = storage.all(State)

    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    tears down a databases connection after every
    completed get request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
