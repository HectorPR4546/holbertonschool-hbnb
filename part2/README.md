# HBnB - Project Setup

This project follows a clean architecture with separation of concerns into:

- **app/**: Main application code
  - **api/v1/**: API endpoints (Flask RESTx)
  - **models/**: Business logic classes (User, Place, etc.)
  - **services/**: Facade pattern to connect everything
  - **persistence/**: In-memory repository for storage

## Business Logic

The models are located in `app/models/` and include:

- `User`: Has name, email, and admin flag.
- `Place`: Has location, price, and owner (User).
- `Review`: Linked to a Place and written by a User.
- `Amenity`: Simple resource like "Wi-Fi" or "Pool".

All models use a common `BaseModel` class with UUIDs and timestamps.

## How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    python run.py
    ```

Visit: `http://127.0.0.1:5000/api/v1/`
