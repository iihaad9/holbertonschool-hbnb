from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data = api.payload

        # هنا نفترض أنك ضفت في الـ Facade دالة create_review(data)
        # وترجع كائن Review
        review = facade.create_review(data)

        if review is None:
            # لو في المستقبل حبيت ترجع كود خطأ أذكى، تقدر تعدل الـ facade
            return {'error': 'Could not create review'}, 400

        # نفترض أن Review فيه to_dict() مثل User
        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload

        updated_review = facade.update_review(review_id, data)
        if not updated_review:
            return {'error': 'Review not found'}, 404

        return updated_review.to_dict(), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # نفترض delete_review يرجع True لو نجح، أو False/None لو ما لقى
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review deleted successfully'}, 200
