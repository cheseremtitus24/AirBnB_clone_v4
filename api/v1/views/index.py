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

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")


@app_views.route('/status', strict_slashes=False)
def status():
    """ Function returns a very basic html string
    that reports a status of ok"""
    return jsonify({'status': 'OK'})
