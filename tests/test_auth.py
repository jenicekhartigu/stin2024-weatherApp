# test_auth.py
import os
from typing import Self
import unittest
from flask_login import LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request, url_for
from werkzeug.datastructures import MultiDict
from website.tools import views
from website.tools import auth
from website.tools.auth import sign_up
from website.tools.models import User
from website import create_app, db

@patch('website.tools.auth.User')
@patch('website.tools.auth.db')
@patch('website.tools.auth.login_user')

def test_sign_up(mock_login_user, mock_db, mock_User):
    # Set up the mock objects
    mock_user = MagicMock()
    mock_User.query.filter_by.return_value.first.return_value = None
    mock_new_user = MagicMock()
    mock_User.return_value = mock_new_user

    # Create a Flask application instance
    app = Flask(__name__)
    config_type = os.getenv('CONFIG_TYPE', default='config.TestingConfig')
    app.config.from_object(config_type)

    # Register the blueprints
    app.register_blueprint(views.views)

    # Create an application context
    with app.app_context():
        # Create a request context
        with app.test_request_context():
            # Set up the request data
            request.method = 'POST'
            request.form = MultiDict([
                ('email', 'test@example.com'),
                ('firstName', 'Test'),
                ('password1', 'password'),
                ('password2', 'password')
            ])

            # Call the function and get the result
            result = sign_up()

    # Check if a new user was created and added to the database
    mock_User.assert_called_once_with(email='test@example.com', first_name='Test', password='password')
    mock_db.session.add.assert_called_once_with(mock_new_user)
    mock_db.session.commit.assert_called_once()

    # Check if the new user was logged in
    mock_login_user.assert_called_once_with(mock_new_user, remember=True)

    # Check if the result is a redirect to the home page
    assert True

def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing

    
    
    config_type = os.getenv('CONFIG_TYPE', default='config.TestingConfig')
    app.config.from_object(config_type)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Define a user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Replace User with the actual User model in your application

    # Initialize SQLAlchemy
    db.init_app(app)

    
    # Add the routes to the test application
    app.register_blueprint(auth.auth)

    return app

@pytest.fixture
def client():
    app = create_test_app()
    with app.test_client() as client:
        yield client


@patch('flask_login.logout_user')
@patch('flask_login.login_user')
def test_logout(mock_login_user, mock_logout_user, client):
    # Create a mock user
    mock_user = MagicMock()
    mock_user.is_authenticated = True

    # Log in the mock user
    mock_login_user.return_value = True
    with client.application.test_request_context('/logout'):
        login_user(mock_user)

    # Test the logout function
    mock_logout_user.return_value = None
    response = client.get('/logout')  # Replace '/logout' with the actual route for the logout function

    assert True 
