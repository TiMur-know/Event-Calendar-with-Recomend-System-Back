from app.models.event import Event, db
from app.database import db
from app.models.user_details import UserDetails, user_details_events
from app.types.EventTypes import EventType
from app.types.PopularityEnum import Popularity
trained_model = None
from app.utils.recomendation import train_recommendation_model, recommend_events as recommend_events_util
def initialize_recommendation_model():
    """
    Initialize and train the recommendation model if not already initialized.
    """
    global trained_model
    if trained_model is None:
        trained_model = train_recommendation_model()

def get_all_events():
    """Retrieve all events."""
    events = Event.query.all()
    return [event.to_dict() for event in events]

def get_event_by_id(event_id):
    """Retrieve a single event by ID."""
    return Event.query.get(event_id)

def create_event(data):
    """Create a new event with standardized event type and popularity."""
    if "event_type" in data and data["event_type"] not in [etype.value for etype in EventType]:
        return {"error": f"Invalid event type: {data['event_type']}"}
    if "popularity" in data and data["popularity"] not in [pop.value for pop in Popularity]:
        return {"error": f"Invalid popularity level: {data['popularity']}"}
    new_event = Event(**data)
    db.session.add(new_event)
    db.session.commit()
    return new_event

def update_event(event_id, data):
    """Update an existing event with standardized event type and popularity."""
    event = Event.query.get(event_id)
    if event:
        if "event_type" in data and data["event_type"] not in [etype.value for etype in EventType]:
            return {"error": f"Invalid event type: {data['event_type']}"}
        if "popularity" in data and data["popularity"] not in [pop.value for pop in Popularity]:
            return {"error": f"Invalid popularity level: {data['popularity']}"}
        for key, value in data.items():
            setattr(event, key, value)
        db.session.commit()
        return event
    return None

def delete_event(event_id):
    """Delete an event by ID."""
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return True
    return False

def subscribe_to_event(event_id, user_id):
    """Subscribe a user to an event."""
    event = Event.query.get(event_id)
    user_details = UserDetails.query.filter_by(user_id=user_id).first()
    if event and user_details:
        if event not in user_details.events:
            user_details.events.append(event)
            event.popularity_count += 1
            db.session.commit()
            return True
    return False

def unsubscribe_from_event(event_id, user_id):
    """Unsubscribe a user from an event."""
    event = Event.query.get(event_id)
    user_details = UserDetails.query.filter_by(user_id=user_id).first()
    if event and user_details:
        if event in user_details.events:
            user_details.events.remove(event)
            event.popularity_count -= 1
            db.session.commit()
            return True
    return False

def get_event_types():
    """
    Retrieve all unique event types.
    """
    return [event_type.value for event_type in EventType]

def recommend_events(user_id, top_n=5):
    """
    Recommend events for a user based on their details and interactions.
    """
    try:
        global trained_model
        if trained_model is None:
            trained_model = train_recommendation_model()

        recommended_event_ids = recommend_events_util(user_id, trained_model, top_n)
        return recommended_event_ids  # Return only the IDs of recommended events
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "An unexpected error occurred: " + str(e)}
