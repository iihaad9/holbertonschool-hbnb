from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(required=False),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
})

update_place_model = api.model('UpdatePlace', {
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'owner_id': fields.String(),
})

@api.route('/')
class PlaceList(Resource):
    def get(self):
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200

    @api.expect(place_model, validate=True)
    def post(self):
        place, err = facade.create_place(api.payload)
        if err == "owner_not_found":
            return {"error": "Owner not found"}, 404
        if err:
            return {"error": err}, 400
        return place.to_dict(), 201

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(update_place_model, validate=True)
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        updated, err = facade.update_place(place_id, api.payload)
        if err == "owner_not_found":
            return {"error": "Owner not found"}, 404
        if err:
            return {"error": err}, 400
        return updated.to_dict(), 200

    def delete(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        facade.delete_place(place_id)
        return "", 204
