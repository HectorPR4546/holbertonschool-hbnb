# Part 4 - Simple Web Client

This directory contains the front-end web client for the HBnB project, developed using HTML5, CSS3, and JavaScript ES6.

## Objectives

- Develop a user-friendly interface following provided design specifications.
- Implement client-side functionality to interact with the back-end API.
- Ensure secure and efficient data handling using JavaScript.
- Apply modern web development practices to create a dynamic web application.

## Implemented Features

- **Design:** Completed HTML and CSS files for Login, List of Places, Place Details, and Add Review pages.
- **Login:** Implemented user authentication with JWT token storage in cookies and redirection upon successful login.
- **List of Places:** Displays a list of places fetched from the API with client-side filtering by price.
- **Place Details:** Shows detailed information for a selected place, including amenities and reviews.
- **Add Review:** Provides a form for authenticated users to submit reviews for places.

## How to Run

1.  Ensure the backend API (from `part2/`) is running.
    ```bash
    cd part2
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 run.py &
    ```
2.  Navigate to the `part4/base_files` directory.
    ```bash
    cd ../part4/base_files
    ```
3.  Start a simple HTTP server to serve the frontend files.
    ```bash
    python3 -m http.server 8000 &
    ```
4.  Open your web browser and navigate to `http://localhost:8000/index.html` or `http://localhost:8000/login.html`.

## Credentials for Testing

- **Email:** `admin@hbnb.io`
- **Password:** `password`

## Notes

- This client interacts with the API running on `http://localhost:5000`.
- CORS has been configured on the backend to allow cross-origin requests from `http://localhost:8000`.
