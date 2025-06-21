#!/usr/bin/python3
"""Initialize the HBnB application package."""
from flask import Flask

app = Flask(__name__)

from app.api import *
from app.business import *
from app.repository import *
