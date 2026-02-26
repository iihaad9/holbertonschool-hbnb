#!/usr/bin/python3
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(required=True, description="Rating of the place (1-5)"),
        "user_id": fields.String(required=True, description="ID of the user"),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)

update_review_model = api.model(
    "UpdateReview",
    {
        "text": fields.String(description="Updated review text"),
        "rating": fields.Integer(description="Updated rating (1-5)"),
    },
)


def _validate_rating(value):
    if value is None:
        return True
    if not isinstance(value, int):
        return False
    return 1 <= value <= 5


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "User or place not found")
    def post(self):
        data = api.payload

        if not _validate_rating(data.get("rating")):
            return {"error": "rating must be an integer between 1 and 5"}, 400

        result = facade.create_review(data)

        if isinstance(result, tuple):
            review, err = result
            if review is None:
                if err in ("user_not_found", "place_not_found"):
                    return {"error": err}, 404
                return {"error": err or "Could not create review"}, 400
        else:
            review = result
            if review is None:
                return {"error": "Could not create review"}, 400

        return review.to_dict(), 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):
    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(update_review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    def put(self, review_id):
        data = api.payload or {}

        if "rating" in data and not _validate_rating(data.get("rating")):
            return {"error": "rating must be an integer between 1 and 5"}, 400

        updated_review = facade.update_review(review_id, data)
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
