#!/usr/bin/python3
""" State Module for HBNB project """
import os
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, VARCHAR, DateTime
from sqlalchemy.orm import backref
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """Amenity class handles all application amenities"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'amenities'
        id = Column(VARCHAR(60), primary_key=True)

        created_at =  Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at =  Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        name = Column(String(128), nullable=False)
        place_amenities = relationship('PlaceAmenity',
                                       backref='amenities',
                                       cascade='delete')
        places = relationship("Place",
                              secondary="place_amenity",
                              back_populates="amenities",
                              overlaps="place_amenities,amenities")

    else:
        name = ''
