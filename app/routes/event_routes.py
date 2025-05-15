from flask import Blueprint, request, jsonify
from app.controllers.event_controller import (
    get_all_events,
    get_event_by_id,
    create_event,
    update_event,
    delete_event,
    subscribe_to_event,
    unsubscribe_from_event,
    recommend_events,
    get_event_types
)
from app.utils.auth import token_required
from app.types.EventTypes import EventType

event_routes = Blueprint('event_routes', __name__)

@event_routes.route('/', methods=['GET'])
def fetch_all_events():
    """Fetch all events."""
    events = get_all_events()
    return jsonify(events), 200

@event_routes.route('/<event_id>', methods=['GET'])
def fetch_event_by_id(event_id):
    """Fetch event by ID."""
    event = get_event_by_id(event_id)
    if event:
        return jsonify(event.to_dict()), 200
    return jsonify({'error': 'Event not found'}), 404

@event_routes.route('/', methods=['POST'])
def create_new_event():
    """Create a new event."""
    data = request.get_json()
    event = create_event(data)
    return jsonify(event.to_dict()), 201

@event_routes.route('/<event_id>', methods=['PUT'])
def modify_event(event_id):
    """Update an event."""
    data = request.get_json()
    event = update_event(event_id, data)
    if event:
        return jsonify(event.to_dict()), 200
    return jsonify({'error': 'Event not found'}), 404

@event_routes.route('/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    """Delete an event."""
    success = delete_event(event_id)
    if success:
        return jsonify({'message': 'Event deleted successfully'}), 200
    return jsonify({'error': 'Event not found'}), 404
@token_required
@event_routes.route('/<event_id>/subscribe', methods=['POST'])
def subscribe_user(event_id):
    """Subscribe a user to an event."""
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    success = subscribe_to_event(event_id, user_id)
    if success:
        return jsonify({'message': 'Subscribed successfully'}), 200
    return jsonify({'error': 'Event not found or subscription failed'}), 404
@token_required
@event_routes.route('/<event_id>/unsubscribe', methods=['POST'])
def unsubscribe_user(event_id):
    """Unsubscribe a user from an event."""
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    success = unsubscribe_from_event(event_id, user_id)
    if success:
        return jsonify({'message': 'Unsubscribed successfully'}), 200
    return jsonify({'error': 'Event not found or unsubscription failed'}), 404

@event_routes.route('/recommend', methods=['POST'])
def get_recommendations():
    """
    Get event recommendations for a user.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    top_n = data.get('top_n', 5)

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    recommendations = recommend_events(user_id, top_n)
    if isinstance(recommendations, dict) and 'error' in recommendations:
        return jsonify(recommendations), 400
    return jsonify({'recommendations': recommendations}), 200
@event_routes.route('/event_types', methods=['GET'])
def fetch_event_types():
    """
    Fetch all unique event types.
    """
    event_types = get_event_types()
    return jsonify({'event_types': event_types}), 200