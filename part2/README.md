# HBnB Project

## Project Overview

This is a simple HBnB (Holberton Airbnb) application built with Flask. The project follows a modular architecture with clear separation of concerns across different layers.

## Project Structure

```text
hbnb/
├── app/
│   ├── __init__.py                 # Flask application factory
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py            # User API endpoints
│   │       ├── places.py           # Place API endpoints
│   │       ├── reviews.py          # Review API endpoints
│   │       ├── amenities.py        # Amenity API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User business logic
│   │   ├── place.py                # Place business logic
│   │   ├── review.py               # Review business logic
│   │   ├── amenity.py              # Amenity business logic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py               # Facade pattern implementation
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py           # In-memory repository
├── run.py                          # Application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Project dependencies
├── README.md                       # Project documentation
```

## Directory Explanation

- **app/**: Contains the core application code
- **api/**: Houses the API endpoints, organized by version (v1/)
- **models/**: Contains the business logic classes
- **services/**: Implements the Facade pattern for layer communication
- **persistence/**: Contains the in-memory repository (will be replaced with database later)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Run the Flask application:
```bash
python run.py
```

2. The application will start in debug mode and be available at:
   - Main app: http://localhost:5000
   - API documentation: http://localhost:5000/api/v1/

## Current Status

This is the initial setup with:
- ✅ Project structure created
- ✅ Flask application configured
- ✅ In-memory repository implemented
- ✅ Facade pattern setup
- ⏳ API endpoints (to be implemented)
- ⏳ Business logic models (to be implemented)
- ⏳ Database integration (to be implemented in Part 3)

## Next Steps

- Implement business logic models (User, Place, Review, Amenity)
- Create API endpoints
- Add validation and error handling
- Integrate database persistence layer