# HBnB Project

## Project Overview

This is a simple HBnB (Holberton Airbnb) application built with Flask. The project follows a modular architecture with clear separation of concerns across different layers.

## Project Structure

```text
part2/
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

## Business Logic Layer

The application includes four main business entities:

### Models

- **User**: Represents users of the application
  - Attributes: `id`, `first_name`, `last_name`, `email`, `is_admin`, `created_at`, `updated_at`
  - Each user can own multiple places and write multiple reviews

- **Place**: Represents rental properties
  - Attributes: `id`, `title`, `description`, `price`, `latitude`, `longitude`, `owner`, `created_at`, `updated_at`
  - Each place belongs to one owner (User) and can have multiple reviews and amenities

- **Review**: Represents reviews written by users for places
  - Attributes: `id`, `text`, `rating`, `place`, `user`, `created_at`, `updated_at`
  - Each review belongs to one user and one place

- **Amenity**: Represents amenities available at places
  - Attributes: `id`, `name`, `created_at`, `updated_at`
  - Can be associated with multiple places (many-to-many relationship)

### Relationships

- **User ↔ Place**: One-to-many (one user can own multiple places)
- **Place ↔ Review**: One-to-many (one place can have multiple reviews)
- **User ↔ Review**: One-to-many (one user can write multiple reviews)
- **Place ↔ Amenity**: Many-to-many (places can have multiple amenities, amenities can be in multiple places)

### Testing Models

Run the model tests to verify everything works:

```bash
python test_models.py
```

## Current Status

This is the current progress:
- ✅ Project structure created
- ✅ Flask application configured
- ✅ In-memory repository implemented
- ✅ Facade pattern setup
- ✅ Business logic models implemented
- ✅ Model relationships working
- ⏳ API endpoints (to be implemented)
- ⏳ Database integration (to be implemented in Part 3)

## Next Steps

- Create API endpoints for all models
- Add input validation and error handling
- Integrate database persistence layer