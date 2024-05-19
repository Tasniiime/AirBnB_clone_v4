#!/usr/bin/python3
"""class for serializing and deserializing objects to a JSON file."""
import json
import os
import datetime


class FileStorage:
    """handles the storage and retrieval of data using JSON serialization."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of all stored objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary with a unique key."""
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes the stored objects to a JSON file."""
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json_objects = {
                key: obj.to_dict() for key, obj in FileStorage.__objects.items()
            }
            json.dump(json_objects, file)

    def reload(self):
        """Deserializes objects from the JSON file and loads them into the storage dict.s"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
            obj_dict = json.load(file)
            FileStorage.__objects = {
                key: self.classes()[data["__class__"]](**data)
                for key, data in obj_dict.items()
            }

    def classes(self):
        """Provides a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        return {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

    def attributes(self):
        """Returns the valid attributes and their types for each class."""
        return {
            "BaseModel": {
                "id": str,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime
            },
            "User": {
                "email": str,
                "password": str,
                "first_name": str,
                "last_name": str
            },
            "State": {
                "name": str
            },
            "City": {
                "state_id": str,
                "name": str
            },
            "Amenity": {
                "name": str
            },
            "Place": {
                "city_id": str,
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
            "Review": {
                "place_id": str,
                "user_id": str,
                "text": str
            }
        }
