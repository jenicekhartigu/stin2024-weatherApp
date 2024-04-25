
import pytest
from unittest.mock import patch
from flask import Flask
from website import create_app

def test_create_app():
    # Call the function and get the result
    app = create_app()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # Check if the result is a Flask application instance
    assert isinstance(app, Flask)

    # Check if the blueprints are registered correctly
    assert 'views' in app.blueprints
    assert 'auth' in app.blueprints