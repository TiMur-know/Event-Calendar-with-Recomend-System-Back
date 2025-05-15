import pytest
from app.types.PopularityEnum import Popularity
from app.types.EventTypes import EventType
import enum

def test_popularity_enum_members():
    assert list(Popularity) == [
        Popularity.LOW,
        Popularity.MEDIUM,
        Popularity.HIGH
    ]

def test_popularity_enum_values():
    assert Popularity.LOW.value == "low"
    assert Popularity.MEDIUM.value == "medium"
    assert Popularity.HIGH.value == "high"

def test_popularity_is_enum():
    assert issubclass(Popularity, enum.Enum)

def test_event_type_enum_members():
    expected = [
        EventType.CONFERENCE,
        EventType.MEETUP,
        EventType.WORKSHOP,
        EventType.SEMINAR,
        EventType.FESTIVAL,
        EventType.CONCERT,
        EventType.SPORTS,
        EventType.WEEKEND
    ]
    assert list(EventType) == expected

def test_event_type_enum_values():
    assert EventType.CONFERENCE.value == "conference"
    assert EventType.MEETUP.value == "meetup"
    assert EventType.WORKSHOP.value == "workshop"
    assert EventType.SEMINAR.value == "seminar"
    assert EventType.FESTIVAL.value == "festival"
    assert EventType.CONCERT.value == "concert"
    assert EventType.SPORTS.value == "sports"
    assert EventType.WEEKEND.value == "weekend"

def test_event_type_is_enum():
    assert issubclass(EventType, enum.Enum)
