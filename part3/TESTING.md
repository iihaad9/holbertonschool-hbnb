# HBnB – Part 2
# Testing and Validation Report

---

## 1. Running the Application

Install dependencies:

pip3 install -r requirements.txt

Run the server:

python3 run.py

Swagger documentation available at:

http://localhost:5000/api/v1/

---

## 2. Automated Unit Tests

All automated tests were implemented using `unittest`.

Run all tests using:

python3 -m unittest discover -s tests -p "test_*.py" -v

### Test Coverage Includes

- Business Logic validation (model-level validation)
- Relationship methods (add_amenity, review linking)
- API endpoint validation
- Correct HTTP status codes
- Error handling

### Test Files

- tests/test_users.py
- tests/test_places.py
- tests/test_amenities.py
- tests/test_reviews.py
- tests/test_models_validation.py
- tests/test_relationships.py

### Business Logic Validation Tests

These tests directly instantiate model classes to validate:

- Invalid email format
- Empty required fields
- Negative price
- Invalid latitude (>90 or <-90)
- Invalid longitude (>180 or <-180)
- Invalid rating (outside 1–5)
- Empty review text

These tests ensure validation exists in the business logic layer, not only at API level.

---

## 3. Manual Testing (Black-Box Testing)

Black-box testing was performed using:

- Swagger UI
- cURL
- Browser requests

Each endpoint was tested for:

- Success cases
- Invalid input
- Missing fields
- Boundary values
- Invalid relationships

---

# USERS

### Create User (201)

POST /api/v1/users/

Expected:
- 201 Created
- Response contains generated id

### Duplicate Email (400)

Expected:
- 400 Bad Request
- { "error": "Email already registered" }

### Invalid Email Format (400)

Expected:
- 400 Bad Request

### Missing Required Fields (400)

Expected:
- 400 Bad Request

### Get User by ID

Expected:
- 200 if exists
- 404 if not found

---

# PLACES

### Create Place (201)

Expected:
- 201 Created
- Owner returned as expanded object
- Amenities returned as list

### Invalid Owner (404)

Expected:
- 404 Not Found

### Boundary Value Testing

Price:
- price = 0 → valid
- price < 0 → 400

Latitude:
- latitude = -90 → valid
- latitude = 90 → valid
- latitude > 90 → 400

Longitude:
- longitude = -180 → valid
- longitude = 180 → valid
- longitude > 180 → 400

### Update Place

Expected:
- 200 OK
- Updated values reflected

### Delete Place

Expected:
- 204 No Content

---

# AMENITIES

### Create Amenity (201)

Expected:
- 201 Created

### Empty Name (400)

Expected:
- 400 Bad Request

### Duplicate Amenity Name (if applicable)

Expected:
- Validation handled correctly

---

# REVIEWS

### Create Review (201)

Expected:
- 201 Created
- Review linked to correct user and place

### Rating Boundary Testing

- rating = 1 → valid
- rating = 5 → valid
- rating = 0 → 400
- rating = 6 → 400

### Missing text (400)

Expected:
- 400 Bad Request

### Invalid user_id / place_id (404)

Expected:
- 404 Not Found

### Get All Reviews (200)

Expected:
- 200 OK
- List returned

---

## 4. Relationship Testing

Relationship behavior validated through automated tests:

- add_amenity correctly attaches amenity to place
- Review correctly links user and place
- No broken references allowed
- Non-existent related entities return proper errors

---

## 5. Validation Summary

The system validates:

- Required fields
- Field types
- Unique email constraint
- Positive numeric values
- Coordinate boundaries
- Rating range (1–5)
- Existence of related entities
- Relationship integrity

All endpoints return appropriate HTTP status codes and properly handle both valid and invalid input.

---

## Conclusion

The API has been validated using:

- Automated unit tests (business logic + API)
- Black-box manual testing
- Boundary value testing
- Relationship integrity testing

All endpoints behave as expected under both normal and edge-case conditions.

---

End of Testing Report.
