#!/usr/bin/python3
"""the module creates a Review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Class  manages revt iew objects"""

    place_id = ""
    user_id = ""
    text = ""
