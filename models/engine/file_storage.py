#!/usr/bin/python3

import json

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = 'file.json'  # JSON file path
    __objects = {}  # Dictionary to store objects

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def all(self, cls=None):
        """Returns a dictionary or a filtered dictionary of models currently in storage."""
        if cls is None:
            return self.__objects.copy()  # Return a copy to prevent direct modification
        else:
            return {key: obj for key, obj in self.__objects.items() if isinstance(obj, cls)}

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside."""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in self.__objects:
            del self.__objects[key]
            self.save()  # Save changes after deletion

    def save(self):
        """Saves the storage dictionary to the JSON file"""
        with open(FileStorage.__file_path, 'w') as f:
            serialized_objects = {}
            for key, obj in self.__objects.items():
                serialized_objects[key] = obj.to_dict()
            json.dump(serialized_objects, f)

    def reload(self):
        """Loads the storage dictionary from the JSON file"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                serialized_objects = json.load(f)
                for key, val in serialized_objects.items():
                    class_name = val['__class__']
                    obj = eval(class_name + '(**val)')
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """Closes the file storage"""
        self.reload()
