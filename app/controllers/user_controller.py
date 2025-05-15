from app.models.user import User
from app.models.user_details import UserDetails
from app.models.token_blacklist import TokenBlacklist  
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def generate_jwt_token(user_id):
    """Generate a JWT token for the given user ID."""
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    return token

def login_user(data):
    """Authenticate user and return user object if valid."""
    try:
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "Email and password are required"}, 400

        user = get_user_by_email(email)
        if not user:
            return {"error": "User not found"}, 404

        if check_password_hash(user.password, password):
            token = generate_jwt_token(user.id)
            user_data, _ = get_user_for_login(email)
            return {"session_token": token, "user": user_data}, 200
        else:
            return {"error": "Invalid password"}, 401
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_user_for_login(email):
    """Get user for login."""
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "User not found"}, 404

    user_details = UserDetails.query.filter_by(user_id=user.id).first()
    if not user_details:
        return {"error": "User details not found"}, 404

    event_ids = [int(event.id) for event in user_details.events] 

    login_user = {
        "id": user.id,
        "fullname": user_details.full_name,
        "eventIds": event_ids,  
        "role": user.role
    }
    print("User data for login:", login_user)
    return login_user, 200

def logout_user(data):
    """Log out user and invalidate session."""
    try:
        session_token = data.get("session_token")
        if not session_token:
            return {"error": "Session token is required"}, 400

        jwt.decode(session_token, SECRET_KEY, algorithms=['HS256'])
        if TokenBlacklist.query.filter_by(token=session_token).first():
            return {"error": "Session token is already invalidated"}, 400

        blacklisted_token = TokenBlacklist(token=session_token)
        db.session.add(blacklisted_token)
        db.session.commit()
        return {"message": "Logged out successfully"}, 200
    except jwt.ExpiredSignatureError:
        return {"error": "Session token has already expired"}, 401
    except jwt.InvalidTokenError:
        return {"error": "Invalid session token"}, 401
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def validate_registration_data(data):
    """Validate registration data."""
    email = data.get("email")
    password = data.get("password") 
    preferred_event_types = data.get("preferred_event_types")

    if not email or not password:
        return {"error": "Email and password are required"}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "User already exists"}, 409
    return None, 200

def registration_user(data):
    """Registration of a new user."""
    try:
        validation_error, status_code = validate_registration_data(data)
        if validation_error:
            return validation_error, status_code
        create_user(data)
        return {"message": "User registered successfully"}, 201
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def hash_password(password):
    """Hash a password using pbkdf2:sha256."""
    return generate_password_hash(password, method='pbkdf2:sha256')

def create_user(data):
    """Create a new user."""
    email = data.get("email")
    password = data.get("password")
    role = "user"  
    preferred_event_types = data.get("prefferedTypes",  [])

    full_name = data.get("fullname")
    hashed_password = hash_password(password)  
    new_user = User(email=email, password=hashed_password, role=role)  
    new_user_details = UserDetails(
        user=new_user,
        full_name=full_name,
        preferred_event_types=preferred_event_types
    )
    db.session.add(new_user)
    db.session.add(new_user_details)
    db.session.commit()

def update_user_details(userId, data):
    """Update user details in the database."""
    try:
        user = User.query.filter_by(id=userId).first()
        if not user:
            return {"error": "User not found"}, 404

        user_details = UserDetails.query.filter_by(user_id=userId).first()
        if not user_details:
            return {"error": "User details not found"}, 404
        
        user_details.full_name = data.get("full_name", user_details.full_name)
        user_details.phone_number = data.get("phone_number", user_details.phone_number)
        user_details.location = data.get("location", user_details.location)
        user_details.sex = data.get("sex", user_details.sex)

        user_details.preferred_event_types = data.get("preferred_event_types", user_details.preferred_event_types)
        user.role = data.get("role", user.role)

        db.session.commit()
        return {"message": "User details updated successfully"}, 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_user_details(userId):
    """Get user details by user ID."""
    try:
        user = User.query.filter_by(id=userId).first()
        if not user:
            return {"error": "User not found"}, 404
        
        user_details = UserDetails.query.filter_by(user_id=userId).first()
        print("User details:", user_details.__dict__)
        if not user_details:
            return {"error": "User details not found"}, 404
        
        send_user_details = {
            "id": user.id,
            "email": user.email,
            "full_name": user_details.full_name,
            "phone_number": user_details.phone_number,
            "sex": user_details.sex,
            "location": user_details.location,
            "preferred_event_types": user_details.preferred_event_types,
        }
        return send_user_details, 200
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_user_by_email(email):
    """Get user by email."""
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    return user
