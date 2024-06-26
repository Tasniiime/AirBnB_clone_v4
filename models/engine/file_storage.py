#!/usr/bin/python3

import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    '''def all(self, cls=None):
        """Returns a list of objects of one type of class"""
        if cls is None:
            return list(FileStorage.__objects.values())
        else:
            return [obj for obj in FileStorage.__objects.values() if isinstance(obj, cls)]'''
    

    def new(self, obj):
        """Adds a new object to storage dictionary"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
    
    def all(self, cls=None):
        """Returns a dictionary or a filtered dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
            return {key: obj for key, obj in FileStorage.__objects.items() if isinstance(obj, cls)}


    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            serialized_objects = {}
            for key, obj in FileStorage.__objects.items():
                serialized_objects[key] = obj.to_dict()
            json.dump(serialized_objects, f)

    def reload(self):
        """Loads storage dictionary from file"""
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
        """Deletes obj from __objects if it's inside"""
        if obj is None:
            return
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in self.__objects:
            del self.__objects[key]

    def close():
        """this method deserialize the json file"""
        self.reload()
