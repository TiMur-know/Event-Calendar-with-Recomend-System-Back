from flask import Blueprint, request, jsonify
from app.controllers.user_controller import (
    update_user_details,
    get_user_details
)
from app.controllers.event_controller import (
    subscribe_to_event,
    unsubscribe_from_event
)
from app.utils.auth import token_required

user_routes = Blueprint('user_routes', __name__)
@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user_detail(user_id):
    """Route for getting user details."""

    response, status_code = get_user_details(user_id)
    print(f"Response from get details: {response}, Status Code: {status_code}")
    if status_code == 200:
        return jsonify(response), status_code
    return jsonify(response), status_code

@user_routes.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    
    """Route for updating user details."""
    data = request.get_json()
    print(f"Data to update: {data}")
    response, status_code = update_user_details(user_id, data)
    return jsonify(response), status_code

@user_routes.route('/unsubscribe', methods=['POST'])
@token_required
def unsubscribe_user(current_user, event_id):
    """Unsubscribe a user from an event."""
    user_id = request.json.get('user_id')
    success = unsubscribe_from_event(event_id, user_id)
    if success:
        return jsonify({'message': 'Unsubscribed successfully'}), 200
    return jsonify({'error': 'Event not found'}), 404

@user_routes.route('/subscribe', methods=['POST'])
@token_required
def subscribe_user(current_user, event_id):
    """Subscribe a user to an event."""
    user_id = request.json.get('user_id')
    success = subscribe_to_event(event_id, user_id)
    if success:
        return jsonify({'message': 'Subscribed successfully'}), 200
    return jsonify({'error': 'Event not found'}), 404