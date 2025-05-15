from app.models.user import User
from app.models.user_details import UserDetails
from app.models.event import Event
from app import create_app
from app.database import db, init_db
from app.types.PopularityEnum import Popularity
from app.types.EventTypes import EventType
from datetime import datetime
from werkzeug.security import generate_password_hash

def hash_password(password):
    """Hash a password using pbkdf2:sha256."""
    return generate_password_hash(password, method='pbkdf2:sha256')

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Seed users
    users = [
        User(id=1, email="test1@gmail.com", password=hash_password("PestPassword23!"), role="admin"),
        User(id=2, email="test@gmail.com", password=hash_password("RestPassword13!"), role="user"),
        User(id=3, email="test56@gmail.com", password=hash_password("TestPassword12!"), role="user"),
        User(id=4, email="user4@example.com", password=hash_password("UserPassword45!"), role="user"),
        User(id=5, email="user5@example.com", password=hash_password("UserPassword55!"), role="user"),
        User(id=6, email="admin2@example.com", password=hash_password("AdminPassword65!"), role="admin"),
        User(id=7, email="user7@example.com", password=hash_password("UserPassword75!"), role="user"),
        User(id=8, email="user8@example.com", password=hash_password("UserPassword85!"), role="user")
    ]
    db.session.bulk_save_objects(users)

    # Seed events
    events = [
        Event(
            id=1, date=datetime.fromisoformat("2025-03-01T00:00:00+00:00"),
            title="Spring Festival", description="Celebrate the arrival of spring with music and food.",
            type=EventType.FESTIVAL.value, popularity=Popularity.HIGH.value,
            popularity_count=1000, location="123 Park Ave, Springfield, IL", duration=8
        ),
        Event(
            id=2, date=datetime.fromisoformat("2025-03-03T00:00:00+00:00"),
            title="Beach Meetup", description="A casual meetup at the beach with games and networking.",
            type=EventType.MEETUP.value, popularity=Popularity.MEDIUM.value,
            popularity_count=500, location="456 Ocean Blvd, Miami, FL", duration=48
        ),
        Event(
            id=3, date=datetime.fromisoformat("2025-03-06T00:00:00+00:00"),
            title="City Center Festival", description="A grand festival in the heart of the city.",
            type=EventType.FESTIVAL.value, popularity=Popularity.HIGH.value,
            popularity_count=1500, location="789 Main St, Metropolis, NY", duration=12
        ),
        Event(
            id=4, date=datetime.fromisoformat("2025-03-10T00:00:00+00:00"),
            title="Stadium Concert", description="An electrifying concert featuring top artists.",
            type=EventType.CONCERT.value, popularity=Popularity.MEDIUM.value,
            popularity_count=800, location="101 Stadium Rd, Capital City, CA", duration=6
        ),
        Event(
            id=5, date=datetime.fromisoformat("2025-03-15T00:00:00+00:00"),
            title="Arena Sports Event", description="A thrilling sports event at the arena.",
            type=EventType.SPORTS.value, popularity=Popularity.HIGH.value,
            popularity_count=1200, location="202 Arena Dr, Gotham, NJ", duration=3
        ),
        Event(
            id=6, date=datetime.fromisoformat("2025-03-20T00:00:00+00:00"),
            title="Tech Conference", description="A conference showcasing the latest in technology.",
            type=EventType.CONFERENCE.value, popularity=Popularity.LOW.value,
            popularity_count=300, location="303 Tech Way, Silicon Valley, CA", duration=24
        ),
        Event(
            id=7, date=datetime.fromisoformat("2025-03-25T00:00:00+00:00"),
            title="Community Workshop", description="A hands-on workshop for community members.",
            type=EventType.WORKSHOP.value, popularity=Popularity.MEDIUM.value,
            popularity_count=600, location="404 Community Ln, Smallville, KS", duration=4
        ),
        Event(
            id=8, date=datetime.fromisoformat("2025-03-30T00:00:00+00:00"),
            title="Library Seminar", description="An educational seminar at the local library.",
            type=EventType.SEMINAR.value, popularity=Popularity.LOW.value,
            popularity_count=200, location="505 Library St, Riverdale, GA", duration=2
        ),
        Event(
            id=9, date=datetime.fromisoformat("2025-04-05T00:00:00+00:00"),
            title="Downtown Festival", description="A vibrant festival in the downtown area.",
            type=EventType.FESTIVAL.value, popularity=Popularity.HIGH.value,
            popularity_count=1800, location="606 Downtown Ave, Star City, TX", duration=10
        ),
        Event(
            id=10, date=datetime.fromisoformat("2025-04-10T00:00:00+00:00"),
            title="Amphitheater Concert", description="A live concert at the amphitheater.",
            type=EventType.CONCERT.value, popularity=Popularity.MEDIUM.value,
            popularity_count=700, location="707 Amphitheater Rd, Central City, CO", duration=5
        ),
        Event(
            id=11, date=datetime.fromisoformat("2025-04-15T00:00:00+00:00"),
            title="National Sports Event", description="A national-level sports event at the stadium.",
            type=EventType.SPORTS.value, popularity=Popularity.HIGH.value,
            popularity_count=1500, location="808 National Stadium Rd, Coast City, FL", duration=4
        ),
        Event(
            id=12, date=datetime.fromisoformat("2025-04-20T00:00:00+00:00"),
            title="City Conference", description="A conference discussing urban development.",
            type=EventType.CONFERENCE.value, popularity=Popularity.LOW.value,
            popularity_count=250, location="909 Conference Hall Rd, Hill Valley, CA", duration=20
        ),
        Event(
            id=13, date=datetime.fromisoformat("2025-04-25T00:00:00+00:00"),
            title="Tech Hub Workshop", description="A workshop on innovative technologies.",
            type=EventType.WORKSHOP.value, popularity=Popularity.MEDIUM.value,
            popularity_count=500, location="1010 Tech Hub Rd, Wakanda, IL", duration=6
        ),
        Event(
            id=14, date=datetime.fromisoformat("2025-04-30T00:00:00+00:00"),
            title="University Seminar", description="A seminar hosted at the university auditorium.",
            type=EventType.SEMINAR.value, popularity=Popularity.LOW.value,
            popularity_count=150, location="1111 University Blvd, Springfield, IL", duration=3
        ),
        Event(
            id=15, date=datetime.fromisoformat("2025-05-05T00:00:00+00:00"),
            title="Central Park Festival", description="A large-scale festival at Central Park.",
            type=EventType.FESTIVAL.value, popularity=Popularity.HIGH.value,
            popularity_count=2000, location="1212 Central Park Ave, Metropolis, NY", duration=12
        ),
        Event(
            id=16, date=datetime.fromisoformat("2025-05-10T00:00:00+00:00"),
            title="Open Air Concert", description="An outdoor concert at the open-air theater.",
            type=EventType.CONCERT.value, popularity=Popularity.MEDIUM.value,
            popularity_count=900, location="1313 Open Air Rd, Gotham, NJ", duration=8
        ),
        Event(
            id=17, date=datetime.fromisoformat("2025-05-15T00:00:00+00:00"),
            title="Stadium Sports Event", description="A sports event at the national stadium.",
            type=EventType.SPORTS.value, popularity=Popularity.HIGH.value,
            popularity_count=1700, location="1414 National Stadium Rd, Star City, TX", duration=5
        ),
        Event(
            id=18, date=datetime.fromisoformat("2025-05-20T00:00:00+00:00"),
            title="Innovation Conference", description="A conference on innovation and creativity.",
            type=EventType.CONFERENCE.value, popularity=Popularity.LOW.value,
            popularity_count=400, location="1515 Innovation Rd, Silicon Valley, CA", duration=18
        ),
        Event(
            id=19, date=datetime.fromisoformat("2025-05-25T00:00:00+00:00"),
            title="Innovation Workshop", description="A workshop on creative problem-solving.",
            type=EventType.WORKSHOP.value, popularity=Popularity.MEDIUM.value,
            popularity_count=700, location="1616 Creative Hub Rd, Riverdale, GA", duration=7
        ),
        Event(
            id=20, date=datetime.fromisoformat("2025-05-30T00:00:00+00:00"),
            title="Auditorium Seminar", description="A seminar at the university auditorium.",
            type=EventType.SEMINAR.value, popularity=Popularity.LOW.value,
            popularity_count=300, location="1717 Auditorium Rd, Hill Valley, CA", duration=4
        )
    ]
    db.session.bulk_save_objects(events)

    user_details = [
        UserDetails(
            id=1, user_id=1, full_name="John Doe", sex="Male", location="New York, NY",
            phone_number="1234567890", preferred_event_types=[EventType.FESTIVAL.value, EventType.MEETUP.value],
            events=[events[0], events[1]]
        ),
        UserDetails(
            id=2, user_id=2, full_name="Jane Smith", sex="Female", location="New York, NY",
            phone_number="1234567890", preferred_event_types=[EventType.FESTIVAL.value],
            events=[events[2]]
        ),
        UserDetails(
            id=3, user_id=3, full_name="Alice Johnson", sex="Female", location="Los Angeles, CA",
            phone_number="9876543210", preferred_event_types=[EventType.WORKSHOP.value, EventType.CONCERT.value],
            events=[]
        ),
        UserDetails(
            id=4, user_id=4, full_name="Bob Brown", sex="Male", location="Chicago, IL",
            phone_number="5551234567", preferred_event_types=[EventType.SPORTS.value, EventType.WEEKEND.value],
            events=[events[1]]
        ),
        UserDetails(
            id=5, user_id=5, full_name="Charlie Davis", sex="Male", location="Houston, TX",
            phone_number="4449876543", preferred_event_types=[EventType.CONFERENCE.value],
            events=[]
        ),
        UserDetails(
            id=6, user_id=6, full_name="Diana Evans", sex="Female", location="San Francisco, CA",
            phone_number="3334567890", preferred_event_types=[EventType.SEMINAR.value, EventType.FESTIVAL.value],
            events=[events[0], events[2]]
        ),
        UserDetails(
            id=7, user_id=7, full_name="Eve Foster", sex="Female", location="Seattle, WA",
            phone_number="2226547890", preferred_event_types=[EventType.MEETUP.value],
            events=[]
        ),
        UserDetails(
            id=8, user_id=8, full_name="Frank Green", sex="Male", location="Miami, FL",
            phone_number="1117894560", preferred_event_types=[EventType.WEEKEND.value, EventType.CONCERT.value],
            events=[events[1]]
        )
    ]
    db.session.bulk_save_objects(user_details)

    db.session.commit()

    print("Database seeded successfully!")
