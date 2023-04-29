#!/usr/bin/python3
'''
    RESTful API for class Place
'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, City, State, Amenity


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    # Check if request data is valid JSON
    if not request.is_json:
        abort(400, description='Not a JSON')
    search_data = request.get_json()

    # Extract search criteria from request data
    states = search_data.get('states', [])
    cities = search_data.get('cities', [])
    amenities = search_data.get('amenities', [])

    # Retrieve all places if no search criteria are provided
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Retrieve places based on search criteria
    places = []
    state_objs = [storage.get(State, state_id) for state_id in states]
    city_objs = [storage.get(City, city_id) for city_id in cities]
    amenity_objs = [storage.get(Amenity, amenity_id) for amenity_id in amenities]

    for state in state_objs:
        if state:
            for city in state.cities:
                if city not in city_objs:
                    city_objs.append(city)

    for city in city_objs:
        if city:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if amenities:
        filtered_places = []
        for place in places:
            if all(amenity in place.amenities for amenity in amenity_objs):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])
