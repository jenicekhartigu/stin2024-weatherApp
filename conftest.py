import pytest
from website import create_app, db

from website.tools.models import User, Places
import os


@pytest.fixture
def app():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    return app

@pytest.fixture(scope='module')
def new_user():
    user = User('testUser', 'Password')
    return user

@pytest.fixture(scope='module')
def new_location():
    user = User('testUser', 'Password')
    new_location = Places('Praha', user)
    return new_location

@pytest.fixture(scope='module')
def test_client():
    # Vytvoření testovací databáze
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()

    # Vytvoření testovacího klienta pomocí Flask aplikace konfigurované pro testování
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # zde probíhá testování
            
            
@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert user data
    default_user = User("testUser", "password")
    second_user = User("testUser1", "password1")
    db.session.add(default_user)
    db.session.add(second_user)

    # Commit the changes for the users
    db.session.commit()

    # Insert book data
    location1 = Places("Praha", default_user)
    location2 = Places("Brno", default_user)
    location3 = Places("Liberec", second_user)
    db.session.add(location1)
    db.session.add(location2)
    db.session.add(location3)

    # Commit the changes for the books
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()