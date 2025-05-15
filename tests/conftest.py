import pytest
from app import create_app
from app.database import db as _db
from flask import Flask

@pytest.fixture(scope="module")
def app():
    app = create_app(testing=True)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
