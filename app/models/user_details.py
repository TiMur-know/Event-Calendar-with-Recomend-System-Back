from app.database import db
from sqlalchemy.orm import relationship

user_details_events = db.Table(
    'user_details_events',
    db.Column('user_details_id', db.Integer, db.ForeignKey('user_details.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

PreferredEventTypesEnum = db.Enum(
    "Concerts",
    "Sports",
    "Theater",
    "Comedy",
    "Festivals",
    "Conventions",
    "Workshops",
    "Exhibitions",
    "Networking",
    "Other"
)

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    sex = db.Column(db.String(10), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    preferred_event_types = db.Column(db.PickleType, nullable=True)

    events = relationship('Event', secondary=user_details_events, backref='user_details')

    user = db.relationship('User', back_populates='details')

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "location": self.location,
            "sex": self.sex,
            "preferred_event_types": self.preferred_event_types if self.preferred_event_types else [],
            "event_ids": [event.id for event in self.events]
        }