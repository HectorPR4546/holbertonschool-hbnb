#!/usr/bin/python3
"""Main application entry point for HBnB project."""

from flask import Flask
from presentation.api.routes import api_blueprint

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
