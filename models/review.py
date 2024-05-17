#!/usr/bin/python3
"""The module creates a review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Class manages review objects"""

    place_id = ""
    user_id = ""
    text = ""
