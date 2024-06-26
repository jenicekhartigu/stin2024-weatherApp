from unittest.mock import patch
from website import *
import pytest

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app



def test_create_app(app):
    assert app
    assert app.config['DEBUG'] is False

def test_blueprint_registration(app):
    assert 'views' in app.blueprints
    assert 'auth' in app.blueprints

def test_app_config(app):
    assert app.config['DEBUG'] is False
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    assert app.config['SECRET_KEY'] == os.getenv('KEY')

# Test that the app uses the correct template folder
def test_app_template_folder(app):
    assert app.template_folder == 'templates'

# Test that the login manager is initialized and configured correctly
def test_login_manager(app):
    from flask_login import LoginManager
    assert isinstance(app.login_manager, LoginManager)
    assert app.login_manager.login_view == 'auth.login'


# Test that blueprints are registered with the correct URL prefixes
def test_blueprint_url_prefixes(app):
    assert app.url_map._rules[0].rule != '/'
    assert app.url_map._rules[1].rule != '/auth'