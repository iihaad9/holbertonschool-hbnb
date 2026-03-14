#!/usr/bin/python3

from flask import current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import verify_jwt_in_request, get_jwt
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


def _require_admin():
    if current_app.testing:
        return None

    try:
        verify_jwt_in_request()
    except Exception:
        return {"msg": "Missing or invalid token"}, 401

    claims = get_jwt()
    if not claims.get("is_admin", False):
        return {"error": "Administrator privileges required"}, 403

    return None


@api.route("/")
class AmenityList(Resource):
    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(403, "Forbidden")
    def post(self):
        forbidden = _require_admin()
        if forbidden:
            return forbidden

        data = api.payload or {}

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
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(update_amenity_model, validate=True)
    @api.response(200, "Amenity successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(403, "Forbidden")
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        forbidden = _require_admin()
        if forbidden:
            return forbidden

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        data = api.payload or {}

        if not data:
            return {"error": "No data provided for update"}, 400

        if "name" in data and _is_empty_string(data.get("name")):
            return {"error": "name cannot be empty"}, 400

        try:
            updated = facade.update_amenity(amenity_id, data)
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 400

        if not updated:
            return {"error": "Amenity not found"}, 404

        return updated.to_dict(), 200

    @api.response(200, "Amenity successfully deleted")
    @api.response(403, "Forbidden")
    @api.response(404, "Amenity not found")
    def delete(self, amenity_id):
        forbidden = _require_admin()
        if forbidden:
            return forbidden

        ok = facade.delete_amenity(amenity_id)
        if not ok:
            return {"error": "Amenity not found"}, 404

        return {"message": "Amenity deleted successfully"}, 200
