from flask import request
from flask_restx import Namespace, Resource, fields

from app.services.facade import facade


api = Namespace("reviews", path="/api/v1/reviews", description="Reviews operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True),
        "rating": fields.Integer(required=True, min=1, max=5),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
    },
)

update_review_model = api.model(
    "UpdateReview",
    {
        "text": fields.String(required=False),
        "rating": fields.Integer(required=False, min=1, max=5),
    },
)


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "User or Place not found")
    def post(self):
        data = api.payload or {}
        review, err = facade.create_review(data)

        if err == "user_not_found":
            return {"error": "User not found"}, 404
        if err == "place_not_found":
            return {"error": "Place not found"}, 404
        if err:
            return {"error": str(err)}, 400

        return review.to_dict(), 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route("/<string:review_id>")
@api.param("review_id", "The review identifier")
class ReviewResource(Resource):
    @api.response(200, "Review retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(update_review_model, validate=True)
    @api.response(200, "Review successfully updated")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    def put(self, review_id):
        data = api.payload or {}
        review, err = facade.update_review(review_id, data)

        if err == "review_not_found":
            return {"error": "Review not found"}, 404
        if err:
            return {"error": str(err)}, 400

        return review.to_dict(), 200

    @api.response(200, "Review successfully deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        ok = facade.delete_review(review_id)
        if not ok:
            return {"error": "Review not found"}, 404
        return {"message": "Review successfully deleted"}, 200
