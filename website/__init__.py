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
    
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)
    
    
    
    from .views import views
    from .auth import auth
    
    db.init_app(app)
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Places

    with app.app_context():
        db.create_all()
            
    login_manager = LoginManager()
    login_manager.login_view = 'auth.nologpage'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
