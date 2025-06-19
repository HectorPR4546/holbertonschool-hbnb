"""API routes for HBnB."""

from flask import Blueprint, jsonify, request
from business_logic.facade import HBNBFacade
from business_logic.services import HBNBService

api_blueprint = Blueprint('api', __name__)
facade = HBNBFacade()
service = HBNBService(facade)

@api_blueprint.route('/objects', methods=['POST'])
def create_object():
    """Create a new object."""
    data = request.get_json()
    obj = service.create_object(data)
    return jsonify(obj.to_dict()), 201

@api_blueprint.route('/objects/<obj_id>', methods=['GET'])
def get_object(obj_id):
    """Get an object by ID."""
    obj = service.get_object(obj_id)
    if obj:
        return jsonify(obj.to_dict())
    return jsonify({"error": "Not found"}), 404

@api_blueprint.route('/objects', methods=['GET'])
def get_all_objects():
    """Get all objects."""
    objects = service.get_all_objects()
    return jsonify({k: v.to_dict() for k, v in objects.items()})
