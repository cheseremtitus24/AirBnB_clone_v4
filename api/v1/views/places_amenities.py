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
    City, State, Amenity, Place, User, Review

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_place_amenities(place_id):
    """ Function returns list of cities by states and
    displays/renders them in a html document.
    when no get parameter is provided it will list all available
    states.
    When a state_id is provided it will list all cities within than state
    When a non_existent state_id is provided (url/states/<invalid_state_id>
    the page displays "Not found!"
    """

    if True:
        if STORAGE_TYPE == "db":
            place = storage.get('Place', place_id)
            if not place:
                abort(404)
            amenities = [amenity.to_dict() for amenity in place.amenities]
        else:
            place = storage.get(Place, place_id)
            if not place:
                abort(404)
            amenities = [storage.get(Amenity, amenity_id).to_dict()
                         for amenity_id in place.amenity_ids]
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def del_place_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object of a Place
    """
    if STORAGE_TYPE == "db":
        place = storage.get('Place', place_id)
        if not place:
            abort(404)
        amenity = storage.get('Amenity', amenity_id)
        if not amenity:
            abort(404)
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        # Handles File Storage
        # storage.get return an object dictionary else None
        place = storage.all(Place).values()
        if not place:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """
    Links an Amenity Object to a Place (many-2-many relationship)
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
        place = storage.get("Place", escape(place_id))
        if not place:
            abort(404)

        amenity = storage.get('Amenity', amenity_id)

        if not amenity:
            abort(404)
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        # Handles File Storage
        # storage.get return an object dictionary else None
        place = storage.get(Place, escape(place_id))
        if not place:
            abort(404)

        amenity = storage.get(Amenity, amenity_id)

        if not amenity:
            abort(404)
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
    # return jsonify(new_object.to_dict()), 201
