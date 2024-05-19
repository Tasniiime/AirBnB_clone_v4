#!/usr/bin/python3
"""The script defines the base model"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:

    """A Class from which all other classes inherit"""

    def __init__(self, *args, **kwargs):
        """Initializes instance attributes attributes

        Args:
            - *args:  arguments
            - **kwargs: dictionary of key-values args
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns official string"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute updated_at"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """converts the intance to dict type_"""

    instance_dict = self.__dict__.copy()
    instance_dict["__class__"] = type(self).__name__
    instance_dict["created_at"] = my_dict["created_at"].isoformat()
    instance_dict["updated_at"] = my_dict["updated_at"].isoformat()
    return instance_dict
