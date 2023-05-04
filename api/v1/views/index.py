#!/usr/bin/python3
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

from flask import jsonify, Blueprint

from models import storage, Amenity, City, Review, State, User, Place

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """ Function returns a very basic html string
    that reports a status of ok"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Function stats - returns the objects count
    of model classes in storage
    """
    if STORAGE_TYPE == "db":
        classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    else:
        classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    num_objs = {}
    for i in range(len(classes)):
        num_objs[names[i]] = storage.count(classes[i])

    return jsonify(num_objs)
