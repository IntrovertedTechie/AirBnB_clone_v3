#!/usr/bin/python3
"""Place view module"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def list_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201



@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Searches for places based on JSON request"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    states = data.get('states')
    cities = data.get('cities')
    amenities = data.get('amenities')

    # If no filter provided, return all places
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    place_ids = set()

    if states:
        # Get all cities that belong to the specified states
        state_cities = set()
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    state_cities.add(city)

        # Add all places from the cities in the specified states
        for city in state_cities:
            place_ids.update([place.id for place in city.places])

    if cities:
        # Add all places from the specified cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                place_ids.update([place.id for place in city.places])

    if amenities:
        # Add all places that have all specified amenities
        amenity_ids = set(amenities)
        for place in storage.all(Place).values():
            if amenity_ids.issubset([amenity.id for amenity in place.amenities]):
                place_ids.add(place.id)

    # Get all places with the specified ids and convert to dict format
    places = [storage.get(Place, id) for id in place_ids]
    places = [place.to_dict() for place in places if place]

    return jsonify(places)
#0
