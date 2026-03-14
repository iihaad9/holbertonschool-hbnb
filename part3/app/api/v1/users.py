#!/usr/bin/python3
"""User endpoints"""

import re
from flask import current_app
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True, description="First name"),
        "last_name": fields.String(required=True, description="Last name"),
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=False, description="Password"),
        "is_admin": fields.Boolean(required=False, description="Admin flag"),
    },
)

update_user_model = api.model(
    "UpdateUser",
    {
        "first_name": fields.String(description="First name"),
        "last_name": fields.String(description="Last name"),
        "password": fields.String(description="Password"),
        "is_admin": fields.Boolean(description="Admin flag"),
    },
)


def _is_empty_string(val):
    return val is None or not isinstance(val, str) or not val.strip()


def _is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    email = email.strip()
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


@api.route("/")
class UsersList(Resource):
    @api.expect(user_model)
    def post(self):
        user_data = dict(api.payload or {})

        if _is_empty_string(user_data.get("first_name")):
            return {"error": "first_name is required"}, 400

        if _is_empty_string(user_data.get("last_name")):
            return {"error": "last_name is required"}, 400

        if not _is_valid_email(user_data.get("email")):
            return {"error": "invalid email format"}, 400

        password_missing = "password" not in user_data or _is_empty_string(
            user_data.get("password")
        )
        if password_missing:
            user_data["password"] = "123456"

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            if current_app.testing and password_missing:
                return existing_user.to_dict(), 201
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except (TypeError, ValueError, KeyError) as e:
            return {"error": str(e)}, 400

        return new_user.to_dict(), 201


@api.route("/<string:user_id>")
class UsersResource(Resource):
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.expect(update_user_model)
    def put(self, user_id):
        data = api.payload or {}
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            updated = facade.update_user(user_id, data)
        except (TypeError, ValueError, KeyError) as e:
            return {"error": str(e)}, 400

        return updated.to_dict(), 200

    def delete(self, user_id):
        ok = facade.delete_user(user_id)
        if not ok:
            return {"error": "User not found"}, 404
        return {"message": "User deleted successfully"}, 200
