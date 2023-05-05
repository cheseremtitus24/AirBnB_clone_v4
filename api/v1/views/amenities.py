#!/usr/bin/python3
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
import os

from flask import jsonify, escape, abort, request, make_response

from api.v1.views import app_views
from models import storage, \
    City, State, Amenity

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """ Function returns list of amenities in json format
    """
    temp = list()

    if True:
        if STORAGE_TYPE == "db":
            amenities = storage.all('Amenity').values()
        else:
            amenities = storage.all(Amenity).values()
            dummy = list()

            for value in amenities:
                dummy.append(value)
            amenities = dummy

        for val in amenities:
            temp.append(val.to_dict())
        if len(temp) < 1:
            abort(404)
        else:
            return jsonify(temp)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    temp = list()

    if True:
        if STORAGE_TYPE == "db":
            amenities = storage.all("Amenity").values()
        else:
            amenities = storage.all(Amenity).values()

            # print(cities)

        for val in amenities:
            if val.id == amenity_id:
                temp.append(val.to_dict())
                break
        if len(temp) < 1:
            abort(404)
        else:
            return jsonify(temp)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    if amenity_id:
        if STORAGE_TYPE == "db":
            del_obj = storage.get("Amenity", escape(amenity_id))
        else:
            # Handles File Storage
            # storage.get return an object dictionary else None
            del_obj = storage.get(Amenity, escape(amenity_id))
        if del_obj:
            # storage.delete returns true on success else false
            del_status = storage.delete(del_obj)
            if del_status:
                return jsonify({})
            else:
                abort(404)
        else:
            abort(404)


@app_views.route('/amenities',
                 strict_slashes=False, methods=['POST'])
def post_amenities():
    """ Creates a new State and initializes it with a state name
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    """

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    new_object = Amenity(**req_json)
    new_object.save()
    if STORAGE_TYPE == "db":
        amenity_obj = storage.get("Amenity", escape(new_object.id))
    else:
        # Handles File Storage
        # storage.get return an object dictionary else None
        amenity_obj = storage.get(Amenity, escape(new_object.id))

    return make_response(jsonify(amenity_obj.to_dict()), 201)
    # return jsonify(new_object.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates a city's values
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    """
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("name") is None:
        abort(400, 'Missing name')
    status = storage.update(Amenity, amenity_id, req_json)

    if status:
        return jsonify(status.to_dict())
    else:
        abort(404)
