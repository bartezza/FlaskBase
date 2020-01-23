
import sys
import logging
import coloredlogs
from flask import Flask
from .config import Config
from .auth import init_login


def create_app():
    the_level = logging.DEBUG
    coloredlogs.install(fmt='[%(name)s %(levelname)s]  %(message)s', stream=sys.stdout, level=the_level)
    # change logging level
    new_log_level = "WARNING"
    loggers = [
        "root"
    ]
    for i in loggers:
        logging.getLogger(i).setLevel(new_log_level)

    _log = logging.getLogger(__name__)

    app = Flask(__name__)
    app.config.from_object(Config)

    init_login(app)

    with app.app_context():
        from .main import main_bp
        app.register_blueprint(main_bp)
        from .auth import auth_bp
        app.register_blueprint(auth_bp)
    return app
