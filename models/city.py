#!/usr/bin/python3
""" City Module for HBNB project """
import os
from datetime import datetime

from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, VARCHAR, DateTime

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if STORAGE_TYPE == "db":
        __tablename__ = 'cities'
        id = Column(VARCHAR(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities', cascade='all, delete, delete-orphan')
    else:
        state_id = ''
        name = ''
        places = []
