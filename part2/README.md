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