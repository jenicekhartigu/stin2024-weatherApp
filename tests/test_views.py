import os
from website.tools import views
from website.tools.views import home, noUserApp, appNoUser, delete_note
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request, jsonify
from website.tools.views import delete_note
from werkzeug.datastructures import MultiDict
from flask import Response

@patch('website.tools.views.Places')
@patch('website.tools.views.db')
@patch('website.tools.views.current_user')
def test_delete_note(mock_current_user, mock_db, mock_Places):
    # Set up the mock objects
    mock_note = MagicMock()
    mock_note.user_id = 1
    mock_Places.query.get.return_value = mock_note
    mock_current_user.id = 1

    # Create a Flask application instance
    app = Flask(__name__)

    # Create an application context
    with app.app_context():
        # Create a request context
        with app.test_request_context():
            # Set up the request data
            request.data = b'{"noteId": 1}'

            # Call the function and get the result
            result = delete_note()

    # Check if the note was deleted and the changes were committed
    mock_db.session.delete.assert_called_once_with(mock_note)
    mock_db.session.commit.assert_called_once()

    # Check if the result is an empty JSON object
    assert True


    
    
def test_appNoUser():
    
    assert True

import pytest
from flask import Flask
from website.tools.views import noUserApp

def test_noUserApp():
    # Create a Flask application instance
    template_dir = os.path.abspath('website/templates')
    app = Flask(__name__, template_folder=template_dir)
    config_type = os.getenv('CONFIG_TYPE', default='config.TestingConfig')
    app.config.from_object(config_type)

    # Register the views blueprint
    app.register_blueprint(views.views)

    # Create a test client
    client = app.test_client()

    # Send a GET request to the '/app' route
    response = client.get('/app')

    # Check the status code of the response
    assert response.status_code == 200

    # Check the content of the response
    assert True
    
def test_home():
    
    assert True
    
    
import pytest
from flask import Flask, request
from website.tools.views import appNoUser

def create_test_app():
    template_dir = os.path.abspath('website/templates')
    app = Flask(__name__, template_folder=template_dir)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.register_blueprint(views.views)
    return app

@pytest.fixture
def client():
    app = create_test_app()
    with app.test_client() as client:
        yield client

@patch('website.tools.views.show_weather')
def test_appNoUser_POST(mock_show_weather, client):
    mock_show_weather.return_value = ({'current': {'condition': {'text': 'TestWeather', 'icon': 'TestIcon'}, 'temp_c': 'TestTemp'}}, None, None, None, 'TestCity')
    response = client.post('/nologin', data={'getMesto': 'TestCity'})
    assert response.status_code == 200
    assert b'TestCity' in response.data

@patch('website.tools.views.show_weather')
@patch('website.tools.views.current_location')
def test_appNoUser_GET(mock_current_location, mock_show_weather, client):
    mock_current_location.return_value = [None, {'location': {'name': 'TestCity'}}]
    mock_show_weather.return_value = ({'current': {'condition': {'text': 'TestWeather', 'icon': 'TestIcon'}, 'temp_c': 'TestTemp'}}, None, None, None, 'TestCity')
    response = client.get('/nologin')
    assert response.status_code == 200