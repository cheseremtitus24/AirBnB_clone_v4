#!/usr/bin/python3
"""
This module Utilizes basic routes and simple
html display and utilizes render_template
which allows rendering of external reference html
files
"""
from flask import Flask, escape, make_response, render_template, jsonify
import os

from api.v1.views import app_views
# from api.v1.views import states
# from api.v1.views import index
import api.v1.views
from models import storage
from models.state import State
from models.city import City
from flask_cors import CORS

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')
SERVE_HOST = os.environ.get('HBNB_API_HOST')
SERVE_PORT = os.environ.get('HBNB_API_PORT')

os.environ["FLASK_APP"] = "app.py"

app = Flask(__name__)
# CORS(app)  # This will enable Cors for all routes
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

"""
 You can customize how the Flask Blueprint extends
  the application by providing some parameters to register_blueprint:

 ->[url_prefix] is an optional prefix for all the Blueprint’s routes.
 ->[subdomain] is a subdomain that Blueprint routes will match.
 ->[url_defaults] is a dictionary with default values for view arguments.

 """
app.register_blueprint(app_views)


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
        flag = True
    else:
        states = storage.all(City).values()
        flag = False
    # cities = storage.state_cities("421a55f4-7d82-47d9-b54c-a76916479545")
    return render_template(
        '8-cities_by_states.html',
        states=states.values(),
        storage=storage,
        city_decision=flag)


@app.route('/states', strict_slashes=False)
@app.route('/states/<text>', strict_slashes=False)
def get_states(text="all"):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    if text == "all":
        if STORAGE_TYPE == "db":
            states = storage.all('State')
        else:
            states = storage.all(State)
        return render_template('7-states_list.html', states=states)

    else:
        if STORAGE_TYPE == "db":
            states = storage.all('State')
            dummy = list()
            for state in states.values():
                if state.id == text:
                    states = state
                    dummy.append(states)

            return render_template(
                '9-states.html',
                states=dummy,
                storage=storage,
                condition=len(dummy))
        else:
            states = storage.all(City).values()
            return render_template(
                '8-cities_by_states.html',
                states=states,
                storage=storage,
                city_decision=0)


@app.route('/hbnb_filters', strict_slashes=False)
def filters_list():
    """
        method to display html page 6-index.html
    """
    states = storage.all('State').values()
    amenities = storage.all('Amenity').values()
    for item in amenities:
        print(item.name)
    return render_template(
        "10-hbnb_filters.html",
        states=states, amenities=amenities)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    tears down a databases connection after every
    completed get request
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    overrides the default 404 not found error
    :param error:
    :return:
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    if SERVE_HOST and SERVE_PORT:
        app.run(host=SERVE_HOST, port=SERVE_PORT, debug=True, threaded=True)
    elif SERVE_PORT:
        app.run(host='0.0.0.0', port=SERVE_PORT, debug=True, threaded=True)
    elif SERVE_HOST:
        app.run(host=SERVE_HOST, port=5000, debug=True, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
