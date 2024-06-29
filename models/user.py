from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base, storage_type
from models.city import Place


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if storage_type == 'db':
        places = relationship("Place", cascade="all, delete", backref="user")
        reviews = relationship("Review", cascade="all, delete", backref="user")
    else:
        @property
        def places(self):
            """Getter attribute that returns the list of Place instances with user_id equals
               to the current User.id"""
            from models import storage
            place_instances = storage.all(Place)
            return [place for place in place_instances.values() if place.user_id == self.id]

        @property
        def reviews(self):
            """Getter attribute that returns the list of Review instances with user_id equals
               to the current User.id"""
            from models import storage
            review_instances = storage.all(Review)
            return [review for review in review_instances.values() if review.user_id == self.id]
