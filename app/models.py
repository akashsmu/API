from enum import unique
from poplib import POP3_SSL_PORT
from tkinter.tix import COLUMN
from .database import Base
from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True , nullable = False)
    title = Column(String, nullable=False)
    content = Column(String,nullable= False)
    published = Column(Boolean, server_default='TRUE',nullable = False)
    create_at = Column(TIMESTAMP(timezone= True),nullable= False,server_default = text('NOW()'))

class User(Base):
    __tablename__ = 'users'

    email  = Column(String,nullable = False, unique = True)
    password = Column(String, nullable = False)
    id = Column(Integer, nullable =False , primary_key = True)
    create_at = Column(TIMESTAMP(timezone= True),nullable= False,server_default = text('NOW()'))

