#!/usr/bin/env python3
"""
This module creates the SQLAlchemy model named User for 
database table named users
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'uses'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=False)
    reset_token= Column(String(250), nullable=False)
