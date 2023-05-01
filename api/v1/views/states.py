# noinspection PyInterpreter,PyInterpreter
"""
This is a module that implements a blueprint
this blueprint is a kind of modularization of
flask applications.
The only requirement is that you will then
import this package file in main then register the
blueprint (app_views) as shown below

app.register_blueprint(app_views)

You can also override its url_prefix like so
app.register_blueprint(app_views, url_prefix="/diff/url")
"""
from flask import jsonify, escape, Blueprint, abort, render_template
from jinja2 import TemplateNotFound
import os


from api.v1.views import app_views
from models import BaseModel, storage, Amenity, City, Review, State, User, Place

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<text>', strict_slashes=False)
def get_states(text="all"):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    temp = list()
    if text == "all":
        if STORAGE_TYPE == "db":
            states = storage.all('State')
        else:
            states = storage.all(State)
        for key, val in states.items():
            temp.append(val.to_dict())
        # return render_template('7-states_list.html', states=states)
        return jsonify(temp)
    else:
        if STORAGE_TYPE == "db":
            states = storage.all('State')
            # cities = storage.state_cities("421a55f4-7d82-47d9-b54c-a76916479545")
            dummy = list()
            for state in states.values():
                if state.id == text:
                    states = state
                    dummy.append(states)
            # for key, val in dummy[0]:
            #     temp.append(val.to_dict())
            if len(dummy) < 1:
                abort(404)
            else:
                return jsonify(dummy[0].to_dict())
            """
            return render_template(
                '9-states.html',
                states=dummy,
                storage=storage,
                condition=len(dummy))
                """
        else:
            states = storage.all(State)
            dummy = list()
            for state in states.values():
                if state.id == text:
                    states = state
                    dummy.append(states)
            # for key, val in dummy[0]:
            #     temp.append(val.to_dict())
            if len(dummy) < 1:
                abort(404)
            else:
                return jsonify(dummy[0].to_dict())

        # states = storage.all(City).values()
        #     return jsonify(states.to_dict())

        # return render_template(
        #     '8-cities_by_states.html',
        #     states=states,
        #     storage=storage,
        #     city_decision=0)


@app_views.route('/states/<string:text>', strict_slashes=False, methods=['DELETE'])
def del_states(text):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    if text:
        if STORAGE_TYPE == "db":
            del_obj = storage.get("State", escape(text))
        else:
            # Handles File Storage
            # storage.get return an object dictionary else None
            del_obj = storage.get(State, escape(text))
        if del_obj:
            # storage.delete returns true on success else false
            del_status = storage.delete(del_obj)
            if del_status:
                return jsonify({})
            else:
                abort(404)
        else:
            abort(404)
