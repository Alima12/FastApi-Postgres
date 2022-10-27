from .db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("UserModel", back_populates="posts")


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    posts = relationship("PostModel", back_populates="owner")
    is_admin = Column(Boolean, server_default="False")


class Vote(Base):
    __tablename__ = "votes"
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


class Tokens(Base):
    __tablename__ = "tokens"
    token = Column(String, primary_key=True)
    user = Column(ForeignKey("users.id", ondelete="CASCADE"))
    is_expired = Column(Boolean, server_default="False")



