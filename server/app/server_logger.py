import logging
import os
from config import Config
from functools import wraps


def setup_logger(name, log_file, level=logging.DEBUG):
    logs_directory = os.path.join(Config.LOGS_DIR)
    os.makedirs(logs_directory, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_file_path = os.path.join(logs_directory, log_file)

    # handler = logging.FileHandler(log_file_path)
    handler = logging.FileHandler(log_file_path, mode="w")

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def log_errors(logger):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger.exception("An error occurred: %s", e)
                # return jsonify({"error": "An unexpected error occurred"}), 500

        return decorated_function

    return decorator
