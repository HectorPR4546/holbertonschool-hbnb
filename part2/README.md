# HBnB - Project Setup

This project follows a clean architecture with separation of concerns into:

- **app/**: Main application code  
  - **api/v1/**: API endpoints using Flask-RESTx  
  - **models/**: Business logic classes (`User`, `Place`, `Amenity`, `Review`)  
  - **services/**: Facade layer for centralized logic and validation  
  - **persistence/**: Handles data storage and retrieval using SQLAlchemy (SQLite for development, MySQL for production)

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

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**

    ```bash
    python run.py
    ```

    This will start the Flask development server. The application will automatically create the `development.db` SQLite database and an initial admin user if they don't exist.

3.  **Access the API:**

    Open your browser or API client and visit:

    ```
    http://127.0.0.1:5000/api/v1/
    ```

    This will show the interactive Swagger UI documentation.

---

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Most endpoints require an `access_token` in the `Authorization` header (e.g., `Authorization: Bearer <YOUR_JWT_TOKEN>`).

### Default Admin User

For development purposes, an admin user is automatically created on first run:

-   **Email:** `admin@hbnb.io`
-   **Password:** `admin`

### Obtaining a JWT Token

To get an `access_token`, send a POST request to the login endpoint:

```bash
curl -X POST 'http://127.0.0.1:5000/api/v1/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "admin@hbnb.io",
  "password": "admin"
}'
```

The response will contain your `access_token`.

---

## Example cURL Commands (with Authentication)

Once you have an `access_token`, you can use it in your requests. Replace `<YOUR_JWT_TOKEN>` with the actual token you received.

### Create a User (Admin privileges required)

```bash
curl -X POST 'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <YOUR_JWT_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "securepassword"
}'
```

### Create a Place (Admin or owner privileges required)

```bash
curl -X POST 'http://127.0.0.1:5000/api/v1/places/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <YOUR_JWT_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Nice Stay",
  "description": "Near the beach",
  "price": 120,
  "latitude": 18.4,
  "longitude": -66.1,
  "owner_id": "<user-id>",
  "amenities": []
}'
```

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