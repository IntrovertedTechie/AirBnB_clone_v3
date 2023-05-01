#!/usr/bin/env python

"""
This module defines the State view for handling RESTFul API actions.

Attributes:
    states_api Blueprint: A Flask Blueprint instance for the State view.

Methods:
    all_states(): Retrieves a list of all state objects.
    single_state(state_id): Retrieves a single state object by state_id.
    create_state(): Creates a new state object.
    update_state(state_id): Updates an existing state object by state_id.
    delete_state(state_id): Deletes an existing state object by state_id.
"""

from flask import abort, jsonify, request, Blueprint

from models import storage, state


states_api = Blueprint("states_api", __name__)


@states_api.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """Retrieves a list of all state objects."""
    states = storage.all(state).values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@states_api.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def single_state(state_id):
    """Retrieves a single state object by state_id."""
    state_obj = storage.get(state, state_id)
    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict())


@states_api.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new state object."""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = state(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@states_api.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates an existing state object by state_id."""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "created_at", "updated_at"]
    state_obj = storage.get(state, state_id)
    if state_obj is None:
        abort(404)
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict())


@states_api.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes an existing state object by state_id."""
    state_obj = storage.get(state, state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200

