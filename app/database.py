from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    """Initialize the database schema."""
    from app.models.user import User
    from app.models.user_details import UserDetails, user_details_events 
    from app.models.event import Event
    from app.models.token_blacklist import TokenBlacklist
    db.create_all()
