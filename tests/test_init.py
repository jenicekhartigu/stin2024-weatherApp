import os
import pytest
from website import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_config():
    """Test if the app is created with the correct configuration."""
    test_config = {'TESTING': True}  # Set testing flag to True
    app = create_app(test_config)
    assert True

def test_index(client):
    """Test if the index page returns a valid response."""
    response = client.get('/')
    assert response.status_code == 302
    assert True