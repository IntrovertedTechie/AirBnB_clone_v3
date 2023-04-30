#!/usr/bin/env python3

"""
Index module
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns a JSON with the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """Returns a JSON with the count of each object type"""
    count_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count_dict)
