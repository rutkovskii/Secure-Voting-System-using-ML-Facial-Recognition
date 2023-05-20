from flask import abort, request, Blueprint, render_template, session, flash, jsonify
from app.database.database import session_scope
from config import Config

from datetime import datetime, timedelta
from flask import jsonify


from app.server_logger import setup_logger, log_errors

endpoints_bp = Blueprint("endpoints_bp", __name__)

logger = setup_logger(__name__, "server.log")

@endpoints_bp.route(Config.INDEX_ROUTE, methods=["GET"])
@log_errors(logger)
def index():
    return "Hello World"


@endpoints_bp.route(Config.VOTE_ROUTE, methods=["GET"])
@log_errors(logger)
def vote():
    """"""
    pass 


@endpoints_bp.route(Config.VERIFY_ROUTE, methods=["GET"])
@log_errors(logger)
def verify_voter():
    pass

