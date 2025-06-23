# HBnB Project - Part 2: Project Setup

This project is the second part of the HBnB (Holberton BnB) application, focusing on setting up a well-organized and modular project structure.

## Project Structure Overview

The project is organized into the following key directories and files:

- `part2/`: The root directory for this part of the project.
  - `app/`: Contains the core application code.
    - `__init__.py`: Initializes the Flask application.
    - `api/`: Houses the API endpoints.
      - `v1/`: Version 1 of the API.
        - `__init__.py`: Package initializer.
        - `users.py`, `places.py`, `reviews.py`, `amenities.py`: Placeholder files for API routes.
    - `models/`: Contains the business logic classes (e.g., User, Place).
      - `__init__.py`: Package initializer.
      - `user.py`, `place.py`, `review.py`, `amenity.py`: Placeholder files for model definitions.
    - `services/`: Where the Facade pattern is implemented.
      - `__init__.py`: Initializes the Facade instance.
      - `facade.py`: Defines the `HBnBFacade` class for inter-layer communication.
    - `persistence/`: Contains the data storage logic.
      - `__init__.py`: Package initializer.
      - `repository.py`: Implements the `InMemoryRepository` for temporary data storage.
  - `run.py`: The entry point for running the Flask application.
  - `config.py`: Used for application configuration and environment settings.
  - `requirements.txt`: Lists all Python packages required for the project.
  - `README.md`: This very file, providing an overview of the project setup.

  ### Core Business Logic Classes (Business Logic Layer)

This section details the core entity classes that form the business logic of the HBnB application. Each class inherits from a `BaseModel` which provides common attributes like a unique `id` (UUID), `created_at` timestamp, and `updated_at` timestamp. Property setters are used extensively for robust input validation.

#### `BaseModel`

* **Location:** `app/models/base_model.py`
* **Purpose:** Provides a common base for all core entities, handling universal attributes such as `id` (a UUID string), `created_at` (timestamp of creation), and `updated_at` (timestamp of last modification). Includes `save()` to update `updated_at` and a generic `update()` method.

#### `User` Class

* **Location:** `app/models/user.py`
* **Purpose:** Represents a user of the HBnB application.
* **Attributes:**
    * `id` (String): Unique identifier (UUID).
    * `first_name` (String): User's first name (required, max 50 chars).
    * `last_name` (String): User's last name (required, max 50 chars).
    * `email` (String): User's email (required, unique, valid format).
    * `is_admin` (Boolean): Administrative privileges (defaults to `False`).
    * `created_at` (DateTime): Timestamp of creation.
    * `updated_at` (DateTime): Timestamp of last update.
* **Validation:** Ensures names are present and within length limits, and email has a valid format. Uniqueness of email is handled at the repository/facade level.

#### `Amenity` Class

* **Location:** `app/models/amenity.py`
* **Purpose:** Represents an amenity available at a place (e.g., Wi-Fi, Parking).
* **Attributes:**
    * `id` (String): Unique identifier (UUID).
    * `name` (String): Name of the amenity (required, max 50 chars).
    * `created_at` (DateTime): Timestamp of creation.
    * `updated_at` (DateTime): Timestamp of last update.
* **Validation:** Ensures name is present and within length limits.

#### `Place` Class

* **Location:** `app/models/place.py`
* **Purpose:** Represents a place available for rent.
* **Attributes:**
    * `id` (String): Unique identifier (UUID).
    * `title` (String): Title of the place (required, max 100 chars).
    * `description` (String): Detailed description (optional).
    * `price` (Float): Price per night (positive value).
    * `latitude` (Float): Latitude coordinate (-90.0 to 90.0).
    * `longitude` (Float): Longitude coordinate (-180.0 to 180.0).
    * `owner` (User): Reference to the `User` who owns the place.
    * `reviews` (List of Review objects): Managed relationship; list of reviews for this place.
    * `amenities` (List of Amenity objects): Managed relationship; list of amenities for this place.
    * `created_at` (DateTime): Timestamp of creation.
    * `updated_at` (DateTime): Timestamp of last update.
* **Validation:** Ensures title, price, coordinates, and owner type are valid.
* **Relationships:**
    * **One-to-Many with `User`:** An `owner` is a `User` instance.
    * **One-to-Many with `Review`:** `add_review()` and `remove_review()` methods manage associated `Review` objects.
    * **Many-to-Many with `Amenity`:** `add_amenity()` and `remove_amenity()` methods manage associated `Amenity` objects, preventing duplicates.

#### `Review` Class

* **Location:** `app/models/review.py`
* **Purpose:** Represents a review given to a `Place` by a `User`.
* **Attributes:**
    * `id` (String): Unique identifier (UUID).
    * `text` (String): Content of the review (required).
    * `rating` (Integer): Rating given (1 to 5).
    * `place` (Place): Reference to the `Place` being reviewed.
    * `user` (User): Reference to the `User` who wrote the review.
    * `created_at` (DateTime): Timestamp of creation.
    * `updated_at` (DateTime): Timestamp of last update.
* **Validation:** Ensures text is present, rating is within range, and `place`/`user` are correct object types.
* **Relationships:**
    * **Many-to-One with `Place`:** A `review` is for one `Place`. The `Review`'s constructor automatically adds itself to the `Place`'s `reviews` list.
    * **Many-to-One with `User`:** A `review` is written by one `User`.

---

## How to Install Dependencies

To get started with the project, you need to install the required Python packages.

1.  Navigate to the `part2/` directory:
    ```bash
    cd part2/
    ```
2.  Install the dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

Once the dependencies are installed, you can run the Flask application:

1.  Ensure you are in the `part2/` directory.
2.  Execute the `run.py` file:
    ```bash
    python run.py
    ```

You should see output from Flask indicating that the development server is running. At this stage, no API routes are functional yet, but this confirms that the basic project structure and setup are correct.