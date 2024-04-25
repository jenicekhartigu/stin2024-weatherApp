from flask import Flask
from flask.testing import FlaskClient
from flask_login import login_user
from werkzeug.datastructures import MultiDict

from website import create_app, db
from website.tools.models import User

import pytest

# Fixture to create a test app
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app

# Fixture to create a test client
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

# Test login function
def test_login(client, app):

    # Test with correct credentials
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert b'Logged in successfully!' in response.data
    
    # Test with incorrect password
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'wrong_password'}, follow_redirects=True)
    assert b'Incorrect password, try again.' in response.data
    
    # Test with non-existing email
    response = client.post('/login', data={'email': 'nonexistent@example.com', 'password': 'password'}, follow_redirects=True)
    assert b'Email does not exist.' in response.data
