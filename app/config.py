
from os import environ


class Config:
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY', "") + "asdksaifdsioj"
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    REMEMBER_COOKIE_NAME = "lolpwn_remember"

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # mongo
    MONGO_HOST = environ.get("MONGO_HOST", "127.0.0.1")
    MONGO_USERNAME = environ.get("MONGO_USERNAME", "username")
    MONGO_PASSWORD = environ.get("MONGO_PASSWORD", "password")
    MONGO_DB_NAME = "lolpwn"


    @staticmethod
    def reload():
        Config.MONGO_HOST = environ.get("MONGO_HOST", "127.0.0.1")
        Config.MONGO_USERNAME = environ.get("MONGO_USERNAME", "username")
        Config.MONGO_PASSWORD = environ.get("MONGO_PASSWORD", "password")
        Config.MONGO_DB_NAME = "lolpwn"
