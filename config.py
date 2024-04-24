import os


class Config(object):
    # load_dotenv(dotenv_path=".env")
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    # SECRET_KEY = os.getenv('SECRET_KEY')
    SECRET_KEY = "12345"
    SQLALCHEMY_DATABASE_URI = os.getenv("CON_STRING")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    DEBUG = True