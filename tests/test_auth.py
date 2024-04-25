# test_auth.py
import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request, url_for
from werkzeug.datastructures import MultiDict
from website.tools import views
from website.tools.auth import sign_up

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
    app.secret_key = os.getenv('KEY')

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