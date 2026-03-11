#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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


def _current_user():
    user_id = get_jwt_identity()
    return facade.get_user(user_id)


@api.route("/")
class PlaceList(Resource):
    @api.response(200, "List of places retrieved successfully")
    def get(self):
        places = facade.get_all_places()
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": float(p.latitude),
                "longitude": float(p.longitude),
            }
            for p in places
        ], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(403, "Forbidden")
    @api.response(404, "Owner or amenity not found")
    def post(self):
        data = dict(api.payload or {})
        claims = get_jwt()
        current_user = _current_user()

        if not current_user:
            return {"error": "User not found"}, 404

        if not claims.get("is_admin", False):
            if data.get("owner_id") != current_user.id:
                return {"error": "You can only create places for your own account"}, 403

        place, err = facade.create_place(data)

        if err == "owner_not_found":
            return {"error": "Owner not found"}, 404
        if err == "amenity_not_found":
            return {"error": "Amenity not found"}, 404
        if err == "invalid_amenities":
            return {"error": "amenities must be a list of valid amenity IDs"}, 400
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

    @jwt_required()
    @api.expect(update_place_model, validate=True)
    @api.response(200, "Place successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(403, "Forbidden")
    @api.response(404, "Place, owner, or amenity not found")
    def put(self, place_id):
        data = dict(api.payload or {})
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        claims = get_jwt()
        current_user = _current_user()

        if not current_user:
            return {"error": "User not found"}, 404

        if not claims.get("is_admin", False):
            if place.owner.id != current_user.id:
                return {"error": "You can only update your own places"}, 403
            if "owner_id" in data and data.get("owner_id") != current_user.id:
                return {"error": "You cannot transfer ownership of the place"}, 403

        msg = _validate_place_update(data)
        if msg:
            return {"error": msg}, 400

        updated, err = facade.update_place(place_id, data)

        if err == "place_not_found":
            return {"error": "Place not found"}, 404
        if err == "owner_not_found":
            return {"error": "Owner not found"}, 404
        if err == "amenity_not_found":
            return {"error": "Amenity not found"}, 404
        if err == "invalid_amenities":
            return {"error": "amenities must be a list of valid amenity IDs"}, 400
        if err:
            return {"error": err}, 400

        return updated.to_dict(), 200

    @jwt_required()
    @api.response(200, "Place successfully deleted")
    @api.response(403, "Forbidden")
    @api.response(404, "Place not found")
    def delete(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        claims = get_jwt()
        current_user = _current_user()

        if not current_user:
            return {"error": "User not found"}, 404

        if not claims.get("is_admin", False):
            if place.owner.id != current_user.id:
                return {"error": "You can only delete your own places"}, 403

        ok = facade.delete_place(place_id)
        if not ok:
            return {"error": "Place not found"}, 404

        return {"message": "Place deleted successfully"}, 200
