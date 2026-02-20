# HBnB Part 2 – Testing & Validation Report

## 1. Running the API

Install dependencies:
pip3 install -r requirements.txt

Run the server:
python3 run.py

Swagger documentation:
http://localhost/api/v1/

---

## 2. Automated Unit Tests

Run tests using:

python3 -m unittest discover tests

Implemented test files:
- tests/test_users.py
- tests/test_places.py

---

## 3. Manual Testing (Swagger / cURL)

### Users

Create User (201)
POST /api/v1/users/

Expected:
- Status code 201
- Response contains user id

Duplicate Email (400)
Expected:
- Status code 400
- Error message: Email already registered

Get All Users (200)
Expected:
- Status code 200
- List of users returned

---

### Places

Create Place (201)
POST /api/v1/places/

Expected:
- Status code 201
- Place object returned
- Owner information expanded in response

Create Place with invalid owner (404)
Expected:
- Status code 404
- Error: Owner not found

Get All Places (200)
Expected:
- Status code 200
- List of places returned

Update Place (200)
Expected:
- Status code 200
- Updated fields returned

Delete Place (204)
Expected:
- Status code 204
