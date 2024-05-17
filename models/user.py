#!/usr/bin/python3
"""The module creates a user class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class for managing user objects"""

    first_name = ""
    last_name = ""
    email = ""
    password = ""
