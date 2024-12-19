from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, UUID, ForeignKey, Boolean

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    full_name = Column(String, nullable=False)


class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)


class Member(Base):
    __tablename__ = "members"

    id = Column(UUID, primary_key=True)
    user = Column(UUID, ForeignKey(User.id), nullable=False)
    team = Column(UUID, ForeignKey(Team.id), nullable=False)

    is_deleted = Column(Boolean, default=False)
