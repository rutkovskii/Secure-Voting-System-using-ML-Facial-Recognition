import os


class Config:
    # Locations
    CLIENT_DIR = os.path.abspath(os.path.dirname(__file__))
    SECURITY_DIR = os.path.join(CLIENT_DIR, "security")
