#!/usr/bin/python3
"""Defines the base class for the application."""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """Base class that other classes will derive from."""

    def __init__(self, *args, **kwargs):
        """Initialize the instance attributes.

        Args:
            *args: List of positional arguments.
            **kwargs: Dictionary of keyword arguments.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Return the string representation of the instance."""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update `updated_at` and save the instance to storage."""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance attributes to a dictionary."""
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = type(self).__name__
        instance_dict["created_at"] = instance_dict["created_at"].isoformat()
        instance_dict["updated_at"] = instance_dict["updated_at"].isoformat()
        return instance_dict
