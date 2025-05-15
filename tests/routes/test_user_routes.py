from flask import Blueprint, request, jsonify
from app.controllers.user_controller import get_user_details, update_user_details

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user_detail(user_id):
    user = get_user_details(user_id)
    return jsonify(user), 200

@user_routes.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = update_user_details(user_id, data)
    return jsonify(updated_user), 200
