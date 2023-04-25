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
from models.city import City
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


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """ Display Listing of all States:
    when storage is db set flag to true else set to false
    When storage is other use the public getter method cities
    """
    if STORAGE_TYPE == "db":
        states = storage.all('State')
        flag = 1
        states = states.values()
    else:
        # obj = State()
        # states = obj.cities
        states = storage.all(City).values()
        # print(states)
        flag = 0

    return render_template(
        '8-cities_by_states.html',
        states=states,
        storage=storage,
        city_decision=flag)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    tears down a databases connection after every
    completed get request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
