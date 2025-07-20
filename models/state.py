#!/usr/bin/python3
""" State Module for HBNB project """
import os
from datetime import datetime

from sqlalchemy.orm import relationship

import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey, VARCHAR, DateTime

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """ State class """
    if STORAGE_TYPE == "db":
        __tablename__ = 'states'
        id = Column(VARCHAR(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='delete')
    else:
        name = ''

        @property
        def cities(self):
            """
                getter method, returns list of City objs from storage
                linked to the current State
            """
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
