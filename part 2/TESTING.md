# HBnB – Part 2
# Testing and Validation Report

---

## 1. Running the Application

Install dependencies:

pip3 install -r requirements.txt

Run the server:

python3 run.py

Swagger documentation available at:

/api/v1/

---

## 2. Automated Unit Tests

Run all tests using:

python3 -m unittest discover tests

Implemented test files:

- tests/test_users.py
- tests/test_places.py
- tests/test_amenities.py
- tests/test_reviews.py

All tests validate:
- Correct HTTP status codes
- Successful object creation
- Validation errors
- Invalid input handling

---

## 3. Manual Testing (Black-Box Testing)

Testing was performed using:
- Swagger UI
- cURL
- Browser

---

# USERS

### Create User (201)

POST /api/v1/users/

Request:
{
  "first_name": "Fahad",
  "last_name": "Alanzi",
  "email": "fahad_test@example.com"
}

Expected:
- 201 Created
- Response contains generated id

---

### Duplicate Email (400)

POST with same email again

Expected:
- 400 Bad Request
- { "error": "Email already registered" }

---

### Get All Users (200)

GET /api/v1/users/

Expected:
- 200 OK
- List of users returned

---

### Get User by ID (200 / 404)

GET /api/v1/users/<user_id>

Expected:
- 200 if exists
- 404 if not found

---

# PLACES

### Create Place (201)

POST /api/v1/places/

Request:
{
  "title": "My First Place",
  "description": "Nice apartment",
  "price": 200,
  "latitude": 24.7,
  "longitude": 46.6,
  "owner_id": "<VALID_USER_ID>"
}

Expected:
- 201 Created
- Response contains place id
- Owner object returned (expanded attributes)

---

### Invalid Owner (404)

POST with fake owner_id

Expected:
- 404 Not Found
- { "error": "Owner not found" }

---

### Get All Places (200)

GET /api/v1/places/

Expected:
- 200 OK
- List of places returned

---

### Update Place (200)

PUT /api/v1/places/<place_id>

Example:
{ "price": 500 }

Expected:
- 200 OK
- Updated value reflected

---

### Delete Place (204)

DELETE /api/v1/places/<place_id>

Expected:
- 204 No Content

---

# AMENITIES

### Create Amenity (201)

POST /api/v1/amenities/

Request:
{
  "name": "WiFi"
}

Expected:
- 201 Created
- Response contains amenity id

---

### Missing Name (400)

POST with empty body {}

Expected:
- 400 Bad Request

---

### Get All Amenities (200)

GET /api/v1/amenities/

Expected:
- 200 OK
- List returned

---

# REVIEWS

### Create Review (201)

POST /api/v1/reviews/

Request:
{
  "text": "Great place!",
  "rating": 5,
  "user_id": "<VALID_USER_ID>",
  "place_id": "<VALID_PLACE_ID>"
}

Expected:
- 201 Created
- Response contains review id

---

### Invalid Rating (400)

POST with rating outside range (e.g., 10)

Expected:
- 400 Bad Request

---

### Get All Reviews (200)

GET /api/v1/reviews/

Expected:
- 200 OK
- List returned

---

## 4. Validation Summary

The API correctly validates:

- Required fields
- Maximum field lengths
- Positive numeric values
- Coordinate ranges
- Unique email constraint
- Rating range (1–5)
- Existence of related entities (owner, user, place)

All endpoints return appropriate HTTP status codes and handle edge cases correctly.

---

End of Testing Report.
