import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Locations
    SERVER_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_DIR = os.path.join(SERVER_DIR, "configs")
    VOLUMES_DIR = os.path.join(SERVER_DIR, "volumes")
    LOGS_DIR = os.path.join(VOLUMES_DIR, "logs")
    APP_DIR = os.path.join(SERVER_DIR, "app")
    COMPARE_DIR = os.path.join(APP_DIR, "compare")

    ENVIRONMENT = os.getenv("ENVIRONMENT")
    DATABASE_URI = "postgresql+psycopg2://ubuntu:ubuntu@postgres:5432/postgresDB"

    # Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Routes
    VOTE_ROUTE = "/vote"
    VERIFY_ROUTE = "/verify-voter"
    INDEX_ROUTE = "/"
