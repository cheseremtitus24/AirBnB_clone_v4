#!/usr/bin/python3
"""This module defines a class User"""
import hashlib
import os
from datetime import datetime

from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, VARCHAR, DateTime

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """
        User class handles all application users
    """
    if STORAGE_TYPE == "db":
        __tablename__ = 'users'
        id = Column(VARCHAR(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', backref='users', cascade='delete')
        reviews = relationship('Review', backref='users', cascade='delete')
        videos = relationship('Video', backref='users', cascade='delete')
        images = relationship('Image', backref='users', cascade='delete')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = hashlib.md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

