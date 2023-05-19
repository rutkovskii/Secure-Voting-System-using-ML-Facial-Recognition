import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# When running run.py
from app.database.models import Base, User
from config import Config
from app.server_logger import setup_logger


# from app.database.database_prefills import prefill_users

logger = setup_logger(__name__, "database.log")

try:
    engine = sqlalchemy.create_engine(Config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    logger.info("Database Created")
except Exception as e:
    logger.error(e)
    logger.error("Database Not Created")
    # Handle error


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

def read_image(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def add_profile_pic(user_id, file_path):
    # read the binary data of the image
    image_data = read_image(file_path)

    with session_scope() as session:
        user = session.query(User).filter(User.id == user_id).one()
        user.profile_pic = image_data
        session.commit()

# Use the function to add a profile picture for a user
add_profile_pic(user_id=1, file_path='/path/to/image.jpg')

# def add_sample_users():
#     with session_scope() as s:
#         s.bulk_save_objects(prefill_users)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# recreate_database()
# add_sample_users()
# add_example_datasamples()