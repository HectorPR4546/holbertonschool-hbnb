#!/usr/bin/python3
"""Entry point for the HBnB application."""
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
