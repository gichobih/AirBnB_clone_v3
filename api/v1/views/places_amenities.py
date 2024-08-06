#!/usr/bin/python3
"""
API endpoints for the Place Amenities
"""
from flask import jsonify, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import getenv

# Added storage type check
storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    """Return all amenities for a given place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # Added handling for FileStorage
    if storage_type == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    else:
        return jsonify([storage.get(Amenity, amenity_id).to_dict() for amenity_id in place.amenity_ids])


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Delete an amenity by its ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    # Added handling for FileStorage
    if storage_type == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """Link an amenity to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    # Added handling for FileStorage
    if storage_type == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201

