import os
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    # Use an in-memory SQLite database for testing isolation
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    # Seed a test user
    user = User(email='test@example.com', password_hash='fakehash', role='donor')
    db.session.add(user)
    db.session.commit()
    return user
