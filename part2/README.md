# HBnB - Project Setup

This project follows a clean architecture with separation of concerns into:

- **app/**: Main application code  
  - **api/v1/**: API endpoints using Flask-RESTx  
  - **models/**: Business logic classes (`User`, `Place`, `Amenity`, `Review`)  
  - **services/**: Facade layer for centralized logic and validation  
  - **persistence/**: In-memory storage (no database used)

---

## Business Logic

The models are located in `app/models/` and include:

- **User**: Has `first_name`, `last_name`, `email`
- **Place**: Includes `title`, `description`, `price`, `latitude`, `longitude`, and links to a `User` and a list of `Amenities`
- **Amenity**: Basic `name` attribute, used to decorate `Place` objects
- **Review**: Contains `text`, `rating`, links to both `User` and `Place`

Each model has:
- A unique UUID `id`
- Timestamps: `created_at`, `updated_at`
- Validation logic built into the constructors

---

## API Documentation

Interactive Swagger documentation is available at:

http://127.0.0.1:5000/api/v1/


---

## Validation Rules

Each model performs basic validation:

- **User**:
  - `first_name`, `last_name`, and `email` must not be empty
  - `email` must be a valid email format
- **Place**:
  - `title` must not be empty
  - `price` must be a positive number
  - `latitude` must be between -90 and 90
  - `longitude` must be between -180 and 180
- **Review**:
  - `text` must not be empty
  - `rating` must be between 1 and 5
  - `user_id` and `place_id` must reference existing entities

If invalid input is submitted, a `400 Bad Request` response is returned.

---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt

    Run the application:

python run.py

Then visit:

http://127.0.0.1:5000/api/v1/

Example cURL Commands

Create a user:

curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'

Create a place:

curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nice Stay",
    "description": "Near the beach",
    "price": 120,
    "latitude": 18.4,
    "longitude": -66.1,
    "owner_id": "<user-id>",
    "amenities": []
  }'

Testing

Unit tests are located in the tests/ folder.

Run all tests with:

python3 -m unittest discover tests

Tests cover:

    Valid and invalid data

    All endpoints (users, places, reviews, amenities)

    Validation logic

    Swagger UI manual testing

Author

Héctor R. Pérez Vélez
Holberton School, Puerto Rico – Cohort 26
GitHub: HectorPR4546