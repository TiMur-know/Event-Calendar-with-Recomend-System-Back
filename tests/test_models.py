import pytest
from datetime import datetime

from app.models.event import Event
from app.models.token_blacklist import TokenBlacklist
from app.models.user_details import UserDetails
from app.models.user import User

# ---------- Event ----------

def test_event_instance_creation():
    event = Event(
        id=1,
        title="Test Event",
        description="Description",
        date=datetime(2025, 5, 10, 14, 0),
        type="conference",
        popularity="medium",
        popularity_count=20,
        location="Kyiv",
        duration=90,
        user_id=2
    )
    assert event.title == "Test Event"
    assert isinstance(event.date, datetime)
    assert event.to_dict()["title"] == "Test Event"

# ---------- TokenBlacklist ----------

def test_token_blacklist_repr():
    token = "fake.jwt.token"
    token_entry = TokenBlacklist(token=token)
    assert token_entry.token == token
    assert isinstance(token_entry.__repr__(), str)
    assert token in repr(token_entry)

# ---------- User ----------

def test_user_instance_creation():
    user = User(
        id=1,
        email="user@example.com",
        password="hashedpassword",
        role="user"
    )
    assert user.email == "user@example.com"
    assert user.role == "user"

# ---------- UserDetails ----------

def test_user_details_to_dict():
    details = UserDetails(
        id=1,
        user_id=1,
        full_name="Test User",
        sex="female",
        location="Lviv",
        phone_number="1234567890",
        preferred_event_types=["Concerts", "Festivals"]
    )
    data = details.to_dict()
    assert data["full_name"] == "Test User"
    assert data["preferred_event_types"] == ["Concerts", "Festivals"]
    assert isinstance(data["event_ids"], list)
