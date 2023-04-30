#!/usr/bin/env python3
"""
Defines the endpoints for the index module.
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """
    Retrieves the API status.

    Returns:
        A JSON object with the API status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Retrieves the count of objects by type.

    Returns:
        A JSON object with the count of objects by type.
    """
    classes = {
        "users": "User",
        "places": "Place",
        "states": "State",
        "cities": "City",
        "amenities": "Amenity",
        "reviews": "Review"
    }

    count_dict = {}

    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])

    return jsonify(count_dict)
