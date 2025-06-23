# HBnB - Project Setup

This project follows a clean architecture with separation of concerns into:

- **app/**: Main application code
  - **api/v1/**: API endpoints (Flask RESTx)
  - **models/**: Business logic classes (User, Place, etc.)
  - **services/**: Facade pattern to connect everything
  - **persistence/**: In-memory repository for storage

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
