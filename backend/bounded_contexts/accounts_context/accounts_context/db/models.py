from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, UUID

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    password = Column(String, nullable=False)
