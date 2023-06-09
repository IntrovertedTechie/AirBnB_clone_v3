#!/usr/bin/python3
'''State view module'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    '''Retrieves the list of all State objects'''
    return jsonify([obj.to_dict() for obj in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''Retrieves a State object'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a State'''
    if not request.is_json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a State object'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
