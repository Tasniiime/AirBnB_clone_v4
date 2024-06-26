#!/usr/bin/python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
# from models.base_model import Base


class DBStorage:
    """New engine DBStorage"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        from models.base_model import Base
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(os.getenv('HBNB_MYSQL_USER'),
                    os.getenv('HBNB_MYSQL_PWD'),
                    os.getenv('HBNB_MYSQL_HOST', 'localhost'),
                    os.getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """Query all objects"""
        from models import base_model
        objs = {}
        classes = [cls] if cls else [base_model.Base, *base_model.Base.__subclasses__()]
        for cl in classes:
            for obj in self.__session.query(cl).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objs[key] = obj
        return objs

    def new(self, obj):
        """Add object to session"""
        self.__session.add(obj)

    def save(self):
        """Commit changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload database"""
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                      expire_on_commit=False))

    def close(self):
        """Close session"""
        self.__session.remove()

