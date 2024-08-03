#!/usr/bin/python3
""" API endpoints for amenities """

from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request
from api.v1.views import app_views

AMENITIES_SEGMENT = 'amenities'


@app_views.route(f'/{AMENITIES_SEGMENT}',
                 methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route(f'/{AMENITIES_SEGMENT}/<amenity_id>',
                 methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(f'/{AMENITIES_SEGMENT}/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(f'/{AMENITIES_SEGMENT}',
                 methods=['POST'])
def create_amenity():
    """Creates a new Amenity"""
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(f'/{AMENITIES_SEGMENT}/<amenity_id>',
                 methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    forbidden_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in forbidden_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
