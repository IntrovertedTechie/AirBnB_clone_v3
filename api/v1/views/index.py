#!/usr/bin/python3
"""
This module creates a Flask Blueprint object named app_views
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Return the status of the API"""
    return jsonify({"status": "OK"})
