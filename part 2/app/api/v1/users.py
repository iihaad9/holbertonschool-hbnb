from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
import re

api = Namespace('users', description='User operations')

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _is_non_empty_string(value):
    return isinstance(value, str) and value.strip() != ""


def _is_valid_email(value):
    return isinstance(value, str) and _EMAIL_RE.match(value.strip()) is not None


user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='Updated first name'),
    'last_name': fields.String(description='Updated last name'),
    'email': fields.String(description='Updated email')
})


@api.route('/')
class UserList(Resource):

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
            for u in users
        ], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        user_data = api.payload

        if not _is_non_empty_string(user_data.get("first_name")):
            return {"error": "first_name is required"}, 400

        if not _is_non_empty_string(user_data.get("last_name")):
            return {"error": "last_name is required"}, 400

        if not _is_valid_email(user_data.get("email")):
            return {"error": "invalid email format"}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201


@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(update_user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        update_data = api.payload or {}

        if "first_name" in update_data and not _is_non_empty_string(update_data.get("first_name")):
            return {"error": "first_name cannot be empty"}, 400

        if "last_name" in update_data and not _is_non_empty_string(update_data.get("last_name")):
            return {"error": "last_name cannot be empty"}, 400

        if "email" in update_data:
            if not _is_valid_email(update_data.get("email")):
                return {"error": "invalid email format"}, 400

            existing_user = facade.get_user_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, update_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
