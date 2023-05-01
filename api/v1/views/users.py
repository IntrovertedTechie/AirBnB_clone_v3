from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from datetime import datetime
import uuid

@app_views.route('/users', methods=['GET'])
def list_users():
    '''Retrieves a list of all User objects'''
    list_users = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''Retrieves a User object'''
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    '''Deletes a User object'''
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    '''Creates a User object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')

    user_dict = request.get_json()
    user_dict['id'] = str(uuid.uuid4())
    user_dict['created_at'] = datetime.now().isoformat()
    user_dict['updated_at'] = datetime.now().isoformat()

    user_obj = User(**user_dict)
    storage.new(user_obj)
    storage.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    '''Updates a User object'''
    user_obj = storage.get("User", user_id)
    if not user_obj:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')

    user_dict = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in user_dict.items():
        if key not in ignore_keys:
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict())

