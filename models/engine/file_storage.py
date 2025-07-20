#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import datetime

from models.base_model import BaseModel
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            dictionary = dict()
            for item in FileStorage.__objects.items():
                if type(item[1]) in [cls]:
                    dictionary[item[0]] = item[1]
                else:
                    continue
            return dictionary

        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from models.image import Image
        from models.video import Video

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review, 'Image': Image,'Video': Video
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

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
                 "text": str},
            "Image":
                {"place_id": str,
                 "user_id": str,
                 "image_url": str},
            "Video":
                {"place_id": str,
                 "user_id": str,
                 "video_url": str}
        }
        return attributes

    def delete(self, obj=None):
        """ Deletes Obj from __objects Global storage Dictionary
        parameters:
        obj [class object] - object to be deleted
        returns: true on success else false
        """
        if obj:

            key = obj.to_dict()['__class__'] + '.' + obj.id
            try:
                del (self.__objects[key])
                self.save()
                return True
            except BaseException:
                return False
                pass
            # del(self.all()[key])
        else:
            return True
            pass

    def close(self):
        """
            calls the reload() method for deserialization from JSON to objects
        """
        self.reload()

    def get(self, cls=None, id=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            for item in FileStorage.__objects.items():
                if type(item[1]) in [cls]:
                    key = str(cls.__name__) + '.' + id
                    # print(key)
                    return self.__objects.get(key, None)
                    break
                else:
                    continue
            return None

        else:
            return FileStorage.__objects

    def count(self, cls=None):
        """
        :param cls:  Defines the Class to which its instance objects to count
        :return: a +ve integer value else zero
        """
        count = 0
        if cls:
            for item in FileStorage.__objects.items():
                if type(item[1]) in [cls]:
                    count += 1
                else:
                    continue
            return count

        else:
            return len(FileStorage.__objects)

    def update(self, obj, idd, req_json, ignore_fields=[]):
        """
        :param req_json: json dictionary
        :param idd:
        :param obj: updates
        :return:
        """
        default_list_ignore = ["__class__", "created_at", "id", "updated_at"]
        default_list_ignore += ignore_fields
        if obj:

            pkey = "{}.{}".format(obj.__name__, idd)

            for key, value in req_json.items():
                if key not in default_list_ignore:
                    try:
                        setattr(self.__class__.__objects[pkey], key, value)
                    except BaseException:
                        return None
            self.save()
            self.reload()
            return self.__class__.__objects[pkey]
        else:

            return None
    def get_engine(self):
        """
            commits all changes of current database session
        """
        return self.__class__.__file_path