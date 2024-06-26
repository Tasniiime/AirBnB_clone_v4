#!/usr/bin/python3
"""The module defines a class User"""
from models.base_model import BaseModel


class User(BaseModel):
    """the class assigns various attributes to the user"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
