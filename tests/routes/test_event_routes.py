# In app/routes/event_routes.py or your equivalent
from flask import Blueprint, request, jsonify
from app.controllers.event_controller import (
    get_all_events, create_event, recommend_events, subscribe_to_event, unsubscribe_from_event
)

event_routes = Blueprint('event_routes', __name__)

@event_routes.route('/', methods=['GET'])
def fetch_all_events():
    events = get_all_events()
    return jsonify(events), 200

@event_routes.route('/', methods=['POST'])
def create_event():
    event_data = request.get_json()
    new_event = create_event(event_data)
    return jsonify(new_event), 201

@event_routes.route('/recommend', methods=['POST'])
def get_event_recommendations():
    recommendation_data = request.get_json()
    recommendations = recommend_events(recommendation_data)
    return jsonify(recommendations), 200

@event_routes.route('/subscribe', methods=['POST'])
def subscribe_user():
    subscription_data = request.get_json()
    subscribe_to_event(subscription_data)
    return jsonify({'message': 'Subscribed to event'}), 200

@event_routes.route('/unsubscribe', methods=['POST'])
def unsubscribe_user():
    unsubscription_data = request.get_json()
    unsubscribe_from_event(unsubscription_data)
    return jsonify({'message': 'Unsubscribed from event'}), 200
