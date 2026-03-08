#!/usr/bin/python3
"""Amenity endpoints"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(required=True, description="Name of the amenity"),
        "description": fields.String(required=False, description="Description"),
    },
)

update_amenity_model = api.model(
    "UpdateAmenity",
    {
        "name": fields.String(required=False, description="Updated name"),
        "description": fields.String(required=False, description="Updated description"),
    },
)


def _is_empty_string(value):
    return isinstance(value, str) and value.strip() == ""


@api.route("/")
class AmenityList(Resource):
    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new amenity"""
        data = api.payload or {}

        # Explicit validation for empty name
        if "name" not in data or _is_empty_string(data.get("name")):
            return {"error": "name is required and cannot be empty"}, 400

        try:
            amenity = facade.create_amenity(data)
        except (TypeError, ValueError, KeyError) as e:
            return {"error": str(e)}, 400

        return amenity.to_dict(), 201


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Retrieve amenity by id"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(update_amenity_model, validate=True)
    @api.response(200, "Amenity successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """Update amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        data = api.payload or {}

        # Must send at least one field
        if not data:
            return {"error": "No data provided for update"}, 400

        # If name provided, it can't be empty
        if "name" in data and _is_empty_string(data.get("name")):
            return {"error": "name cannot be empty"}, 400

        try:
            updated = facade.update_amenity(amenity_id, data)
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 400

        if not updated:
            return {"error": "Amenity not found"}, 404

        return updated.to_dict(), 200
