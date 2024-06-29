#!/usr/bin/python3

import json


class FileStorage:
    """The class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a filtered dictionary of models currently in storage.
        If cls is provided, return objects of that type only."""
        if cls is None:
            return FileStorage.__objects
        else:
            return {key: obj for key, obj in FileStorage.__objects.items() if isinstance(obj, cls)}

    def new(self, obj):
        """Add a new object to storage dict"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Save storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            serialized_objects = {}
            for key, obj in FileStorage.__objects.items():
                serialized_objects[key] = obj.to_dict()
            json.dump(serialized_objects, f)

    def reload(self):
        """Load storage dictionary from file"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                serialized_objects = json.load(f)
                for key, val in serialized_objects.items():
                    class_name = val['__class__']
                    obj = eval(class_name + '(**val)')
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if found"""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in self.__objects:
            del self.__objects[key]

    def close(self):
        """Deserialize the JSON file to objects"""
        self.reload()
