#!/usr/bin/python3
"""
This module instantiates a Flask application.
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the database at the end of the request."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors with a custom JSON response."""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
