#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
})

update_amenity_model = api.model('UpdateAmenity', {
    'name': fields.String(description='Updated name'),
    'description': fields.String(description='Updated description')
})


@api.route('/')
class AmenityList(Resource):
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': a.id,
                'name': a.name,
                'description': getattr(a, 'description', None)
            }
            for a in amenities
        ], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        amenity_data = api.payload

        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name,
            'description': getattr(new_amenity, 'description', None)
        }, 201


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': getattr(amenity, 'description', None)
        }, 200

    @api.expect(update_amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update amenity details"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        update_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, update_data)

        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name,
            'description': getattr(updated_amenity, 'description', None)
        }, 200
