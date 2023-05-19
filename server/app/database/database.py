import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# When running run.py
from app.database.models import Base
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


# def add_sample_users():
#     with session_scope() as s:
#         s.bulk_save_objects(prefill_users)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# recreate_database()
# add_sample_users()
# add_example_datasamples()
