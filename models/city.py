#!/usr/bin/python3
"""The module creates a User class"""

from models.base_model import BaseModel


class City(BaseModel):
    """This Class for managing city objects"""

    state_id = ""
    name = ""
