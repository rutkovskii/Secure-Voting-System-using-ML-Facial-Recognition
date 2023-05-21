from flask import abort, request, Blueprint, jsonify
from app.database.database import session_scope
from app.database.models import People
from config import Config

from flask import jsonify
from app.utils import verify_voter_func, accept_vote_func
from app.security.encryption import encrypt_data
from app.security.decryption import decrypt_data_full


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
    logger.info("Received request to vote")

    if request.method == "POST":
        data = request.get_data(as_text=True)

        if not data:
            abort(400, "No body provided")

        # Decrypt the body
        payload = decrypt_data_full(data)

        logger.info("Successfully decrypted data")

        # Accept the vote
        reply = accept_vote_func(payload)

        logger.info("Successfully accepted vote")

        # Encrypt reply
        encrypt_reply = encrypt_data(reply)

        logger.info("Successfully encrypted reply")

        return jsonify(encrypt_reply)

    else:
        abort(400, "Invalid request method")


@endpoints_bp.route(Config.VERIFY_ROUTE, methods=["POST"])
@log_errors(logger)
def verify_voter():
    """Verify the voter's identity."""
    if request.method == "POST":
        try:
            data = request.get_data(as_text=True)
            if not data:
                abort(400, "No body provided")

            payload = decrypt_data_full(data)
            reply = verify_voter_func(payload)
            encrypt_reply = encrypt_data(reply)
            return jsonify(encrypt_reply)

        except Exception as e:
            abort(400, str(e))
    else:
        abort(400, "Invalid request method")


@endpoints_bp.route(Config.RESULTS_ROUTE, methods=["GET"])
@log_errors(logger)
def results():
    """Get the results of the election."""

    with session_scope() as session:
        results = (
            session.query(People).filter_by(voted=True).order_by(People.voted_for).all()
        )

        canditates = {}

        for result in results:
            if result.voted_for in canditates:
                canditates[result.voted_for] += 1
            else:
                canditates[result.voted_for] = 1

        results = [canditates, f"total: {len(results)}"]

        return results
