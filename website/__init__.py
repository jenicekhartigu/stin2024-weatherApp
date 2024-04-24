from flask import Flask
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from os import path
import os

from .person import Person

db = SQLAlchemy()
DB_NAME = "database.db"

__all__ = ("Person",)



def create_app():
    app = Flask(__name__)
    # app.secret_key = "s424724BDJBKjkjky"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = "12345"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Places
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.nologpage'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
        app.config.from_object(config_type)

        with app.app_context():
            db.create_all()
        print('Created Database!')