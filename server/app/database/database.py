import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# When running run.py
from app.database.models import Base, People
from config import Config
from app.server_logger import setup_logger

logger = setup_logger(__name__, "database.log")


def read_image(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def add_profile_pic(file_path):
    # read the binary data of the image
    image_data = read_image(file_path)
    return image_data


def prefill_people():
    return [
        People(
            first_name="Aleksei",
            last_name="Rutkovskii",
            voter_id="32369635",
            profile_pic=add_profile_pic("app/database/assets/Aleksei.jpg"),
            voted=False,
        ),
        People(
            first_name="Daniel",
            last_name="Doe",
            voter_id="0000",
            profile_pic=add_profile_pic("app/database/assets/Daniel.jpg"),
            voted=False,
        ),
        People(
            first_name="Brayden",
            last_name="Doe",
            voter_id="0001",
            profile_pic=add_profile_pic("app/database/assets/Brayden.jpg"),
            voted=False,
        ),
    ]


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


try:
    engine = sqlalchemy.create_engine(Config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    logger.info("Database Created")

    # check if People table is empty
    with session_scope() as s:
        if s.query(People).first() is None:
            # add people
            people = prefill_people()
            s.bulk_save_objects(people)
            logger.info("People Added to the Database")
except Exception as e:
    logger.error(e)
    logger.error("Database Not Created")


# recreate_database()
# add_sample_users()
# add_example_datasamples()
