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
from flask import jsonify, Blueprint

from models import storage, Amenity, City, Review, State, User, Place

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")


@app_views.route('/status', strict_slashes=False)
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
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)
