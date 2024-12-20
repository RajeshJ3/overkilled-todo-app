from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, UUID, Boolean, ForeignKey

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    full_name = Column(String, nullable=False)


class TodoCategory(Base):
    __tablename__ = "todo_categories"

    id = Column(UUID, primary_key=True)
    user = Column(UUID, ForeignKey(User.id), nullable=False)

    name = Column(String, nullable=False)

    is_deleted = Column(Boolean, default=False)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUID, primary_key=True)
    category = Column(UUID, ForeignKey(TodoCategory.id), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    is_completed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
