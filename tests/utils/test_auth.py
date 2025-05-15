import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
import jwt

from app.utils.auth import token_required

SECRET_KEY = "testsecret"

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True

    @app.route('/protected')
    @token_required
    def protected_route(current_user):
        return jsonify({"message": f"Hello {current_user.email}"}), 200

    return app

def generate_token(user_id):
    return jwt.encode({"user_id": user_id}, SECRET_KEY, algorithm="HS256")

def test_token_required_valid_token(app):
    valid_token = generate_token(1)

    with patch("app.utils.auth.SECRET_KEY", SECRET_KEY), \
         patch("app.utils.auth.TokenBlacklist.query") as mock_blacklist, \
         patch("app.utils.auth.User.query") as mock_user_query:
        
        mock_blacklist.filter_by.return_value.first.return_value = None
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user_query.get.return_value = mock_user

        client = app.test_client()
        response = client.get('/protected', headers={"Authorization": f"Bearer {valid_token}"})
        
        assert response.status_code == 200
        assert response.get_json()["message"] == "Hello test@example.com"

def test_token_required_missing_token(app):
    client = app.test_client()
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token is missing!"

def test_token_required_invalid_token(app):
    with patch("app.utils.auth.SECRET_KEY", SECRET_KEY):
        client = app.test_client()
        response = client.get('/protected', headers={"Authorization": "Bearer invalid.token.value"})
        assert response.status_code == 401
        assert response.get_json()["error"] == "Invalid token!"

def test_token_required_expired_token(app):
    expired_token = jwt.encode(
        {"user_id": 1, "exp": 0}, SECRET_KEY, algorithm="HS256"
    )  # expired immediately

    with patch("app.utils.auth.SECRET_KEY", SECRET_KEY):
        client = app.test_client()
        response = client.get('/protected', headers={"Authorization": f"Bearer {expired_token}"})
        assert response.status_code == 401
        assert response.get_json()["error"] == "Token has expired!"

def test_token_required_blacklisted_token(app):
    token = generate_token(1)

    with patch("app.utils.auth.SECRET_KEY", SECRET_KEY), \
         patch("app.utils.auth.TokenBlacklist.query") as mock_blacklist, \
         patch("app.utils.auth.User.query"):
        
        mock_blacklist.filter_by.return_value.first.return_value = True

        client = app.test_client()
        response = client.get('/protected', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 401
        assert response.get_json()["error"] == "Token has been invalidated!"

def test_token_required_user_not_found(app):
    token = generate_token(123)

    with patch("app.utils.auth.SECRET_KEY", SECRET_KEY), \
         patch("app.utils.auth.TokenBlacklist.query") as mock_blacklist, \
         patch("app.utils.auth.User.query") as mock_user_query:
        
        mock_blacklist.filter_by.return_value.first.return_value = None
        mock_user_query.get.return_value = None

        client = app.test_client()
        response = client.get('/protected', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404
        assert response.get_json()["error"] == "User not found!"
