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
    City, State, Amenity, Place, User

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
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
            cities = storage.city_places(city_id).values()
        else:
            cities = storage.all(Place).values()
            dummy = list()

            for value in cities:
                # print(" --------", value)
                if getattr(value, 'city_id', None) == city_id:
                    dummy.append(value)
            cities = dummy

        for val in cities:
            temp.append(val.to_dict())
        if len(temp) < 1:
            abort(404)
        else:
            return jsonify(temp)


# Very dangerous due to DOS - this is because
# The server has to send alot of data to client


@app_views.route('/places', strict_slashes=False)
@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id=None):
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
            cities = storage.all("Place").values()
        else:
            cities = storage.all(Place).values()

            # print(cities)

        for val in cities:
            if place_id is None:
                temp.append(val.to_dict())
            else:
                if val.id == place_id:
                    temp.append(val.to_dict())
                    break
        if len(temp) < 1:
            abort(404)
        else:
            if place_id:
                return jsonify(temp[0])
            else:
                return jsonify(temp)


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_place(place_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """
    if place_id:
        if STORAGE_TYPE == "db":
            del_obj = storage.get("Place", escape(place_id))
        else:
            # Handles File Storage
            # storage.get return an object dictionary else None
            del_obj = storage.get(Place, escape(place_id))
        if del_obj:
            # storage.delete returns true on success else false
            del_status = storage.delete(del_obj)
            if del_status:
                return jsonify({})
            else:
                abort(404)
        else:
            abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def post_places(city_id):
    """ Creates a new Place within a City and initializes it with a state name
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    """

    """
    1. Query all Users =  curl localhost:5000/api/v1/users
      e.g id= 2655e743-ff9e-4837-ac09-1dadf9f7ea26
    2. Query all Cities =  curl localhost:5000/api/v1/cities
    e.g id = 32b7129c-154c-4636-b95b-704d1e45f159
    3. Add a new Place =
    > curl -X POST
    http://0.0.0.0:5000/api/v1/cities/32b7129c-154c-4636-b95b-704d1e45f159/places
    -H "Content-Type: application/json"
    -d '{"name": "bujumbura", "user_id":
    "2655e743-ff9e-4837-ac09-1dadf9f7ea26"}'
    4. Query for all places to check your added
    place 'bujumbura' using    curl localhost:5000/api/v1/cities
    5. or query for all places in with the state
    id of 32b7129c-154c-4636-b95b-704d1e45f159
    > curl localhost:5000/api/v1/
    cities/32b7129c-154c-4636-b95b-704d1e45f159/places


    """

    if STORAGE_TYPE == "db":
        city_obj = storage.get("City", escape(city_id))
    else:
        # Handles File Storage
        # storage.get return an object dictionary else None
        city_obj = storage.get(City, escape(city_id))
    if city_obj is None:
        # If the city_id is not linked to any City object,
        # raise a 404 error
        abort(404, 'Not found')

    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')

    if req_json.get("name") is None:
        abort(400, 'Missing name')
    if req_json.get("user_id") is None:
        abort(400, 'Missing user_id')
    user_id = req_json.get('user_id')
    if STORAGE_TYPE == "db":
        user_obj = storage.get("User", user_id)
    else:
        user_obj = storage.get(User, user_id)

    if user_obj is None:
        # If the city_id is not linked to any City object,
        # raise a 404 error
        abort(404, 'Not found')

    req_json["city_id"] = city_id
    req_json["user_id"] = user_id
    new_object = Place(**req_json)
    new_object.save()
    if STORAGE_TYPE == "db":
        place_obj = storage.get("Place", escape(new_object.id))
    else:
        # Handles File Storage
        # storage.get return an object dictionary else None
        place_obj = storage.get(Place, escape(new_object.id))

    return make_response(jsonify(place_obj.to_dict()), 201)
    # return jsonify(new_object.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ Updates a city's values
    if requested dictionary is none output 'Not a JSON'
    if post data does not contain the key 'name' output 'Missing name'
    On success return a status of 201 else 400
    """
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    ignore_fields = ['city_id', 'user_id']
    status = storage.update(Place, place_id, req_json)

    if status:
        return jsonify(status.to_dict())
    else:
        abort(404)
