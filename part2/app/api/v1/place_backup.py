#!/usr/bin/python3
"""Place endpoints"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("places", description="Place operations")

place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(required=False, description="Description"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude (-90 to 90)"),
        "longitude": fields.Float(required=True, description="Longitude (-180 to 180)"),
        "owner_id": fields.String(required=True, description="Owner user id"),
        "amenities": fields.List(
            fields.String,
            required=False,
            description="List of amenity ids",
        ),
    },
)

update_place_model = api.model(
    "UpdatePlace",
    {
        "title": fields.String(description="Updated title"),
        "description": fields.String(description="Updated description"),
        "price": fields.Float(description="Updated price"),
        "latitude": fields.Float(description="Updated latitude (-90 to 90)"),
        "longitude": fields.Float(description="Updated longitude (-180 to 180)"),
        "owner_id": fields.String(description="Updated owner user id"),
        "amenities": fields.List(
            fields.String,
            required=False,
            description="Updated list of amenity ids",
        ),
    },
)


def _validate_place_update(data):
    if "price" in data:
        price = data.get("price")
        if not isinstance(price, (int, float)) or float(price) <= 0:
            return "price must be a positive number"

    if "latitude" in data:
        lat = data.get("latitude")
        if not isinstance(lat, (int, float)) or not (-90.0 <= float(lat) <= 90.0):
            return "latitude must be between -90.0 and 90.0"

    if "longitude" in data:
        lon = data.get("longitude")
        if not isinstance(lon, (int, float)) or not (-180.0 <= float(lon) <= 180.0):
            return "longitude must be between -180.0 and 180.0"

    if "title" in data:
        title = data.get("title")
        if title is not None and (not isinstance(title, str) or not title.strip()):
            return "title cannot be empty"
        if isinstance(title, str) and len(title.strip()) > 100:
            return "title max length is 100"

    return None


@api.route("/")
class PlaceList(Resource):
    @api.response(200, "List of places retrieved successfully")
    def get(self):
        places = facade.get_all_places()

        result = []
        for p in places:
            result.append(
                {
                    "id": p.id,
                    "title": p.title,
                    "latitude": float(p.latitude),
                    "longitude": float(p.longitude),
                }
            )
        return result, 200

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner or amenity not found")
    def post(self):
        data = api.payload or {}

        place, err = facade.create_place(data)

        if err == "owner_not_found":
            return {"error": "Owner not found"}, 404
        if err == "amenity_not_found":
            return {"error": "Amenity not found"}, 404
        if err:
            return {"error": err}, 400

        return place.to_dict(), 201


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(update_place_model, validate=True)
    @api.response(200, "Place successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place or owner or amenity not found")
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        data = api.payload or {}

        msg = _validate_place_update(data)
        if msg:
            return {"error": msg}, 400

        updated, err = facade.update_place(place_id, data)

        if err == "owner_not_found":
            return {"error": "Owner not found"}, 404
        if err == "amenity_not_found":
            return {"error": "Amenity not found"}, 404
        if err:
            return {"error": err}, 400

        return updated.to_dict(), 200
