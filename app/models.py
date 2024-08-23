from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

"""

Creating the database models

"""

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable = True)
    created_at = Column(DateTime, nullable = True, server_default = 'now()')
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    user = relationship("User")


class User(Base):
    __tablename__ = 'users'
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    id = Column(Integer, primary_key = True, nullable = False)
    created_at = Column(DateTime, nullable = True, server_default = 'now()')



class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete = "CASCADE"), primary_key = True)
