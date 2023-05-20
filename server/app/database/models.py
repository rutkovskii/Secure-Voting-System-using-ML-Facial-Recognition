from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    LargeBinary,
)


Base = declarative_base()


class People(Base):
    __tablename__ = "People"
    id = Column(Integer, primary_key=True)  # This is a new line
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    state = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    voter_id = Column(String, nullable=False)
    profile_pic = Column(LargeBinary, nullable=True)
    voted = Column(Boolean, nullable=False, default=False)
    voted_for = Column(String, nullable=True)
    token = Column(String, nullable=False)

    def __repr__(self):
        return f"<Person {self.first_name} {self.last_name}>"

    def get_profile_pic(self):
        return self.profile_pic
