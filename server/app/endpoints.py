from flask import abort, request, Blueprint, jsonify
from app.database.database import session_scope
from config import Config

from flask import jsonify
from app.utils import verify_voter_func, accept_vote_func
from app.security.encryption import encrypt_data
from app.security.decryption import decrypt_data


from app.server_logger import setup_logger, log_errors

endpoints_bp = Blueprint("endpoints_bp", __name__)

logger = setup_logger(__name__, "server.log")


@endpoints_bp.route(Config.INDEX_ROUTE, methods=["GET"])
@log_errors(logger)
def index():
    return "Hello World"


@endpoints_bp.route(Config.VOTE_ROUTE, methods=["POST"])
@log_errors(logger)
def vote():
    """"""
    if request.method == "POST":
        data = request.get_json()

        if not data:
            abort(400, "No body provided")

        # Decrypt the body
        decrypted_data = decrypt_data(data)

        # Accept the vote
        reply = accept_vote_func(decrypted_data)

        # Encrypt reply
        encrypt_reply = encrypt_data(reply)

        return jsonify(encrypt_reply)

    else:
        abort(400, "Invalid request method")


@endpoints_bp.route(Config.VERIFY_ROUTE, methods=["POST"])
@log_errors(logger)
def verify_voter():
    """Verify the voter's identity."""

    if request.method == "POST":
        data = request.get_json()

        if not data:
            abort(400, "No body provided")

        # Decrypt the body
        decrypted_data = decrypt_data(data)

        # Verify the voter
        reply = verify_voter_func(decrypted_data)

        # Encrypt reply
        encrypt_reply = encrypt_data(reply)

        # Return the reply
        return jsonify(encrypt_reply)

    else:
        abort(400, "Invalid request method")
