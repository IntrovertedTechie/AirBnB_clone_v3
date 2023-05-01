#!/usr/bin/python3
"""
Defines the RESTful API actions for State objects.
"""
from api.v1.views import app_views

from flask import jsonify, abort, request

from models import storage

from models.state import State

from datetime import datetime

import uuid




@app_views.route('/states/', methods=['GET'])

def list_states():
    """
    Retrieves a list of all State objects
    """
    list_states = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(list_states)

@app_views.route('/states', methods=['GET'])
def get_states():
    """
    Retrieves the list of all State objects
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    '''Creates a State'''
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

