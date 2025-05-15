from flask import Blueprint, request, jsonify
from app.controllers.user_controller import login_user, logout_user, registration_user

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    """Route for user login."""
    data = request.get_json()
    response, status_code = login_user(data)
    print("Response from login_user:", response) 
    return jsonify(response), status_code

@auth_routes.route('/logout', methods=['POST'])
def logout():
    """Route for user logout."""
    data = request.get_json()
    response = logout_user(data)
    return jsonify(response), 200

@auth_routes.route('/registration', methods=['POST'])
def register():

    """Route for user registration."""
    data = request.get_json()
    
    response, status_code = registration_user(data)
    print("regssa",response)
    return jsonify(response), status_code
