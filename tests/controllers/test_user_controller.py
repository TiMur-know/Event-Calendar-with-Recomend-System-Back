import pytest
from unittest.mock import patch, MagicMock
from app.controllers import user_controller as uc
from app.models.user import User
from app.models.user_details import UserDetails
from app.models.token_blacklist import TokenBlacklist

@pytest.fixture
def fake_user():
    user = MagicMock(spec=User)
    user.id = 1
    user.email = "test@example.com"
    user.password = uc.hash_password("test123")
    user.role = "user"
    return user
@pytest.fixture
def fake_user_details():
    details = MagicMock(spec=UserDetails)
    details.full_name = "John Doe"
    details.events = []
    details.user_id = 1
    details.preferred_event_types = ["music"]
    return details

@pytest.fixture
def app():
    from app import create_app
    app = create_app(testing=True)
    with app.app_context():
        yield app

def test_login_success(monkeypatch, fake_user, fake_user_details, app):
    with app.app_context():
        monkeypatch.setattr(uc, "get_user_by_email", lambda email: fake_user)
        monkeypatch.setattr(uc, "get_user_for_login", lambda email: ({"id": 1, "fullname": "John Doe", "eventIds": [], "role": "user"}, 200))
        data = {"email": "test@example.com", "password": "test123"}
        response, status = uc.login_user(data)
        assert status == 200
        assert "session_token" in response

def test_login_invalid_password(monkeypatch, fake_user, app):
    with app.app_context():
        monkeypatch.setattr(uc, "get_user_by_email", lambda email: fake_user)
        data = {"email": "test@example.com", "password": "wrongpass"}
        response, status = uc.login_user(data)
        assert status == 401
        assert response["error"] == "Invalid password"

def test_registration_duplicate_user(app):
    with app.app_context(), patch.object(User, 'query') as mock_query:
        mock_query.filter_by.return_value.first.return_value = True
        data = {"email": "test@example.com", "password": "123"}
        error, status = uc.validate_registration_data(data)
        assert status == 409
        assert error["error"] == "User already exists"

def test_logout_user_valid(monkeypatch, app):
    with app.app_context():
        token = uc.generate_jwt_token(1)
        monkeypatch.setattr(TokenBlacklist.query, "filter_by", lambda **kwargs: MagicMock(first=lambda: None))
        monkeypatch.setattr(uc.db.session, "add", lambda x: None)
        monkeypatch.setattr(uc.db.session, "commit", lambda: None)
        response, status = uc.logout_user({"session_token": token})
        assert status == 200
        assert response["message"] == "Logged out successfully"

def test_get_user_details_success(app, fake_user, fake_user_details):
    with app.app_context(), \
         patch.object(User, 'query') as user_query_mock, \
         patch.object(UserDetails, 'query') as details_query_mock:

        user_query_mock.filter_by.return_value.first.return_value = fake_user
        details_query_mock.filter_by.return_value.first.return_value = fake_user_details

        response, status = uc.get_user_details(1)
        assert status == 200
        assert response["email"] == "test@example.com"
        assert response["full_name"] == "John Doe"
