#!/usr/bin/python3
"""
Database engine
"""

import os
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import datetime


class DBStorage:
    """
        handles long term storage of all class instances
    """
    classes = {
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }

    """
        handles storage for database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
            creates the engine self.__engine
        """
        self.__class__.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')), pool_pre_ping=True)

        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__class__.__engine)

    def all(self, cls=None):
        """
           returns a dictionary of all objects
        """
        obj_dict = {}
        if cls is not None:
            try:
                a_query = self.__class__.__session.query(DBStorage.classes[cls])
            except:
                return {}
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

        for c in DBStorage.classes.values():
            a_query = self.__class__.__session.query(c)
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
        return obj_dict

    def state_cities(self, state_id):
        """
        cls is the state id to be searched for
        returns a dictionary of all Cities within a State
        """
        obj_dict = {}
        if state_id is not None:
            a_query = self.__class__.__session.query(City).join(
                State, City.state_id == State.id).filter(
                State.id.in_(
                    (state_id,)))
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

    def city_places(self, city_id):
        """
        cls is the state id to be searched for
        returns a dictionary of all places within a City
        """
        obj_dict = {}
        if city_id is not None:
            a_query = self.__class__.__session.query(Place).join(
                City, Place.city_id == City.id).filter(
                City.id.in_(
                    (city_id,)))
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

    def place_reviews(self, place_id):
        """
        cls is the state id to be searched for
        returns a dictionary of all places within a City
        """
        obj_dict = {}
        if place_id is not None:
            a_query = self.__class__.__session.query(Review).join(
                Place, Place.id == Review.place_id).filter(
                Place.id.in_(
                    (place_id,)))
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

    def new(self, obj):
        """
            adds objects to current database session
        """
        self.__class__.__session.add(obj)

    def save(self):
        """
            commits all changes of current database session
        """
        self.__class__.__session.commit()

    def rollback_session(self):
        """
            rollsback a session in the event of an exception
        """
        self.__class__.__session.rollback()

    def delete(self, obj=None):
        """
            deletes obj from current database session if not None
        """
        if obj:
            self.__class__.__session.delete(obj)
            self.save()
            return True
        return False

    def reload(self):
        """
           creates all tables in database & session from engine
        """
        Base.metadata.create_all(self.__engine)
        self.__class__.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
            calls remove() on private session attribute (self.session)
        """
        self.__class__.__session.close()

    def get(self, cls=None, id=None):
        """
            retrieves one object based on class name and id
        """
        if cls and id:
            fetch = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch)
        return None

    def count(self, cls=None):
        """
            returns the count of all objects in storage
        """
        if cls:
            return len(self.all(cls))
        else:
            return len(self.all())

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                {"id": str,
                 "created_at": datetime.datetime,
                 "updated_at": datetime.datetime},
            "User":
                {"email": str,
                 "password": str,
                 "first_name": str,
                 "last_name": str
                 },
            "State":
                {"name": str},
            "City":
                {"state_id": str,
                 "name": str},
            "Amenity":
                {"name": str},
            "Place":
                {"city_id": str,
                 "user_id": str,
                 "name": str,
                 "description": str,
                 "number_rooms": int,
                 "number_bathrooms": int,
                 "max_guest": int,
                 "price_by_night": int,
                 "latitude": float,
                 "longitude": float,
                 "amenity_ids": list
                 },
            "Review":
                {"place_id": str,
                 "user_id": str,
                 "text": str}
        }
        return attributes

    def update(self, obj, idd, req_json, ignore_fields=[]):
        """
        :param obj: updates
        :return:
        """
        default_list_ignore = ["__class__", "created_at", "id", "updated_at"]
        default_list_ignore += ignore_fields
        if obj:
            # update row to database
            row = self.__session.query(obj).filter_by(id=idd).first()
            # print("Result of no row results is ",row)
            if row:
                # print('original:', row.id, row.name)
                for key, value in req_json.items():
                    if key not in default_list_ignore:
                        setattr(row, key, value)
                self.save()
                return row
            else:
                return None
        else:

            return None
