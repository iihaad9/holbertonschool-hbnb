#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(required=True, description="Rating between 1 and 5"),
        "user_id": fields.String(required=True, description="User ID"),
        "place_id": fields.String(required=True, description="Place ID"),
    },
)

update_review_model = api.model(
    "UpdateReview",
    {
        "text": fields.String(description="Updated review text"),
        "rating": fields.Integer(description="Updated rating between 1 and 5"),
    },
)


@api.route("/")
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    @api.response(201, "Review created successfully")
    @api.response(400, "Invalid input data")
    @api.response(404, "User or Place not found")
    def post(self):
        data = api.payload

        result = facade.create_review(data)

        if isinstance(result, tuple):
            review, error = result
            if review is None:
                if error in ("user_not_found", "place_not_found"):
                    return {"error": error}, 404
                return {"error": error}, 400
        else:
            review = result

        return review.to_dict(), 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):

    @api.response(200, "Review retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(update_review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    def put(self, review_id):
        updated_review = facade.update_review(review_id, api.payload)
        if not updated_review:
            return {"error": "Review not found"}, 404
        return updated_review.to_dict(), 200

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
