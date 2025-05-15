from flask import request
import jwt
from functools import wraps
from app.models.token_blacklist import TokenBlacklist
from app.models.user import User
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def token_required(f):
    """Decorator to validate Bearer token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print("req",request.headers)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return {"error": "Token is missing!"}, 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if TokenBlacklist.query.filter_by(token=token).first():
                return {"error": "Token has been invalidated!"}, 401
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return {"error": "User not found!"}, 404
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired!"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token!"}, 401
        return f(current_user, *args, **kwargs)
    return decorated
