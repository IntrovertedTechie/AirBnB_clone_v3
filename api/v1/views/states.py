#!/usr/bin/python3
"""
States module
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieve the list of all State objects
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieve a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object
    """
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    state = State(**request.json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200