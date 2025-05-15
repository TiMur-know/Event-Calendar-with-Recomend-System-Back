from app.database import db
from datetime import datetime

class TokenBlacklist(db.Model):
    """Model for storing invalidated JWT tokens."""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), nullable=False, unique=True)
    blacklisted_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TokenBlacklist token={self.token}>"
