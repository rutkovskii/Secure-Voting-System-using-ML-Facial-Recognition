from app.database.database import session_scope
from app.database.models import People
import boto3
import secrets
import os
import base64
from app.rekognition.rekognition_image_detection import RekognitionImage
from config import Config
from app.server_logger import setup_logger
from dotenv import load_dotenv

logger = setup_logger(__name__, "utils.log")

load_dotenv()


def accept_vote_func(data):
    """Accept the vote."""

    logger.info("Accepting vote")

    with session_scope() as session:
        voter = (
            # Check based on voter_id and name
            session.query(People)
            .filter_by(
                token=data["token"],
            )
            .first()
        )

        logger.info("Successfully queried database")

        if not voter:
            return {"accepted": False, "error": "Voter not found"}

        logger.info("Successfully found voter")

        if voter.voted:
            return {"accepted": False, "error": "Voter has voted"}

        # Update the voter's voted status
        voter.voted = True
        voter.voted_for = data["voted_for"]

        # Commit the changes
        session.commit()

        logger.info("Successfully committed changes")

        return {"accepted": True, "error": None}


def verify_voter_func(data):
    """Verify the voter's identity."""

    logger.info("Verifying voter")

    with session_scope() as session:
        voter = (
            # Check based on voter_id and name
            session.query(People)
            .filter_by(
                first_name=data["first_name"],
                last_name=data["last_name"],
                voter_id=data["voter_id"],
            )
            .first()
        )

        if not voter:
            return {"verified": False, "token": None, "error": "Voter not found"}

        if voter.voted:
            return {"verified": False, "token": None, "error": "Voter has voted"}

        # Compare the image data
        match = False
        voting_image = data["image_data"]
        profile_image = voter.profile_pic

        # save images locally to read, compare, and delete
        match = saveNcompare(profile_image, voting_image)

        if not match:
            return {"verified": False, "token": None, "error": "Images do not match"}

        # Generate a token
        token = generate_random_string()

        # Update the voter's token
        voter.token = token

        # Commit the changes
        session.commit()

        logger.info("Voter verified")

        return {"verified": True, "token": token, "error": None}


def compare_images(profile_image_path, voting_image_path):
    """Compare two images."""

    rekognition_client = boto3.client(
        "rekognition", region_name=os.getenv("AWS_REGION")
    )

    profile_image_aws = RekognitionImage.from_file(
        profile_image_path, rekognition_client
    )

    voting_image = RekognitionImage.from_file(voting_image_path, rekognition_client)

    matches, unmatches = profile_image_aws.compare_faces(
        target_image=voting_image, similarity=80
    )

    # True if there is a match and not +2 people
    return True if (len(matches) != 0 and len(unmatches) == 0) else False


def generate_random_string(length=8):
    """
    Generates a random string of the specified length.
    """
    return secrets.token_hex(length)


def saveNcompare(profile_image, voting_image_base64):
    rand_str = generate_random_string()

    # save images locally to read
    profile_image_path = os.path.join(
        Config.COMPARE_DIR, f"profile_image_{rand_str}.jpg"
    )
    with open(profile_image_path, "wb") as f:
        f.write(profile_image)  # write bytes directly

    voting_image_path = os.path.join(Config.COMPARE_DIR, f"voting_image_{rand_str}.jpg")
    with open(voting_image_path, "wb") as f:
        voting_image = base64.b64decode(
            voting_image_base64.split(",")[-1]
        )  # Decode the base64 image
        f.write(voting_image)

    match = compare_images(profile_image_path, voting_image_path)

    # delete images
    os.remove(profile_image_path)
    os.remove(voting_image_path)

    return match
