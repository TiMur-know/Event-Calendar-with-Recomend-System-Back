from app.database import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    popularity = db.Column(db.String(50), nullable=False)
    popularity_count = db.Column(db.Integer, nullable=False, default=0)
    location = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('events', lazy=True))

    def to_dict(self):
        """Convert the Event object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'type': self.type,
            'popularity': self.popularity,
            'popularity_count': self.popularity_count,
            'location': self.location,
            'duration': self.duration
        }
