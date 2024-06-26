#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage.

        Args:
            cls (class, optional): If specified, filters the result to include
                only objects of the specified class.

        Returns:
            dict: A dictionary containing objects in storage.
        """
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls)
            if cls and issubclass(cls, BaseModel):
                return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {key: val.to_dict() for key, val in self.__objects.items()}
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file."""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = val['__class__']
                    if cls_name in classes:
                        self.__objects[key] = classes[cls_name](**val)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside.

        Args:
            obj: The object to delete.
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Deserializing the JSON file to objects"""
        self.reload()
