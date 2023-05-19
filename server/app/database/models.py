from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, Date, Time, Boolean
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String(150))
    is_admin = Column(Boolean, nullable=False, default=False)
    auth_token = Column(String, nullable=False)
    datetime_joined = Column(
        String, nullable=False, default=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )  # .isoformat(' ', 'seconds'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_token(self, token):
        return self.auth_token == token

    def get_auth_token(self):
        return self.auth_token

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    def get_is_admin(self):
        return self.is_admin

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "datetime_joined": self.datetime_joined,
        }

    def __repr__(self):
        return "<User(id='{}',<User(name='{}', phone_number='{}', email='{}', datetime_joined='{}')>".format(
            self.id, self.name, self.phone_number, self.email, self.datetime_joined
        )
