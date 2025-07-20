#!/usr/bin/python3
""" Video module for the HBNB project """
import os
from datetime import datetime

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, VARCHAR, DateTime

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class Video(BaseModel, Base):
    """Video class handles all application videos"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'videos'
        id = Column(VARCHAR(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        video_url = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ''
        user_id = ''
        video_url = ''
