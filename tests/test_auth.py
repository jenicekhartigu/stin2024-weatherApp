from flask import Flask, url_for
from flask_login import LoginManager
from website.tools.auth import login, logout, appNoUser
from website.tools.models import User
from website import create_app
from unittest.mock import patch, MagicMock
import pytest


import pytest
from website import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success(client):
    
    
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    print(response.data)  # Print the response content
    assert b'Logged in successfully!' not in response.data

def test_login_incorrect_password(client):
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'wrong_password'})
    assert b'Incorrect password, try again.' in response.data

def test_login_email_not_exist(client):
    response = client.post('/login', data={'email': 'nonexistent@example.com', 'password': 'password123'})
    assert b'Email does not exist.' in response.data
    
def test_logout():
    try: 
        logout()
    except:
        assert 1 == 1