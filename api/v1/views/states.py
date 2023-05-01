#!/usr/bin/env python

"""
This module defines the State view for handling RESTFul API actions.
"""

from flask import abort, jsonify, request, Blueprint

from models import storage, State


states_api = Blueprint("states_api", __name__)


@states_api.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """Retrieves a list of all State objects."""
    states = storage.all(State).values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@states_api.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def single_state(state_id):
    """Retrieves a single State object by state_id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@states_api.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new State object."""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@states_api.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates an existing State object by state_id."""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "created_at", "updated_at"]
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())


@states_api.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes an existing State object by state_id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

