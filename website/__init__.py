from flask import Flask
import os
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, template_folder='templates')

    config_type = os.getenv('CONFIG_TYPE', default='config.TestingConfig')
    app.config.from_object(config_type)
    
    from .tools.views import views
    from .tools.auth import auth
    
    db.init_app(app)
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .tools.models import User, Places

    with app.app_context():
        db.create_all()
            
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

