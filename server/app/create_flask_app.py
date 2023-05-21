# from config import Config

from flask import Flask
from flask_bootstrap import Bootstrap
from sys import set_int_max_str_digits

from app.server_logger import setup_logger
from app.endpoints import endpoints_bp
from config import Config

logger = setup_logger(__name__, "server.log")
logger.info("Logger Created")


# Secret Key
bootstrap = Bootstrap()


def register_blueprints(app):
    app.register_blueprint(endpoints_bp)


def add_configs(app):
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    return app


def create_app():
    FlaskApp = Flask(__name__)
    FlaskApp = add_configs(FlaskApp)
    bootstrap.init_app(FlaskApp)
    logger.info("Flask App Created")
    set_int_max_str_digits(1000000000)
    return FlaskApp


if Config.ENVIRONMENT == "development":
    FlaskApp = create_app()
    register_blueprints(FlaskApp)
    logger.info("Flask App Created in Development Mode")
