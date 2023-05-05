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
    User

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/users', strict_slashes=False)
def get_users():
    """ Function returns list of amenities in json format
    """
    temp = list()

    if True:
        if STORAGE_TYPE == "db":
            users = storage.all('User').values()
        else:
            users = storage.all(User).values()
            dummy = list()

            for value in users:
                dummy.append(value)
            users = dummy

        for val in users:
            temp.append(val.to_dict())
        if len(temp) < 1:
            abort(404)
        else:
            return jsonify(temp)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
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
            user = storage.all("User").values()
        else:
            user = storage.all(User).values()

        for val in user:
            if val.id == user_id:
                temp.append(val.to_dict())
                break
        if len(temp) < 1:
            abort(404)
        else:
            return jsonify(temp[0])


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_user(user_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    if user_id:
        if STORAGE_TYPE == "db":
            del_obj = storage.get("User", escape(user_id))
        else:
            # Handles File Storage
            # storage.get return an object dictionary else None
            del_obj = storage.get(User, escape(user_id))
        if del_obj:
            # storage.delete returns true on success else false
            del_status = storage.delete(del_obj)
            if del_status:
                return jsonify({})
            else:
                abort(404)
        else:
            abort(404)


@app_views.route('/users',
                 strict_slashes=False, methods=['POST'])
def post_users():
    """ Creates a new State and initializes it with a state name
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    """

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if req_json.get("email") is None:
        abort(400, 'Missing email')
    if req_json.get("password") is None:
        abort(400, 'Missing password')
    new_object = User(**req_json)
    new_object.save()
    if STORAGE_TYPE == "db":
        user_obj = storage.get("User", escape(new_object.id))
    else:
        # Handles File Storage
        # storage.get return an object dictionary else None
        user_obj = storage.get(User, escape(new_object.id))

    return make_response(jsonify(user_obj.to_dict()), 201)
    # return jsonify(new_object.to_dict()), 201


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ Updates a city's values
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    TEST:
 curl -X POST http://0.0.0.0:5000/api/v1/users -H
  "Content-Type: application/json" -d
  '{"email": "paris@main", "password": "parris"}'
curl -X PUT http://0.0.0.0:5000/api/v1/users/
3c7b8afe-b947-4c17-99cb-20b58ac67f05
 -H "Content-Type: application/json" -d
 '{"email": "paris@main", "password": "parrisdfsdfis"}'
    """
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    ignore_fields = ['email']
    status = storage.update(User, user_id, req_json, ignore_fields)

    if status:
        return jsonify(status.to_dict())
    else:
        abort(404)
