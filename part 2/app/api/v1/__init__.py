#!/usr/bin/python3
from flask_restx import Api

from app.api.v1.users import api as users_api
from app.api.v1.amenities import api as amenities_api
from app.api.v1.places import api as places_api
from app.api.v1.reviews import api as reviews_api

api = Api(
    title="HBnB API",
    version="1.0",
    description="HBnB Evolution API"
)

api.add_namespace(users_api, path="/api/v1/users")
api.add_namespace(amenities_api, path="/api/v1/amenities")
api.add_namespace(places_api, path="/api/v1/places")
api.add_namespace(reviews_api, path="/api/v1/reviews")
