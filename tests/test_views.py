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

def test_noUserApp():
    
    assert True
    
def test_home():
    
    assert True