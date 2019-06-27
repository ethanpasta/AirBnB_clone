#!/usr/bin/python3
"""Base model class:
   This class is base class for all other class of AirBnB project"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Base model class"""

    def __init__(self):
        """Initialization method for instance"""
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __str__(self):
        """Str method for Base class"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute
        updated_at with the current datetime"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Method returns a dictionary containing all keys/values
        of __dict__ instance"""
        my_dict = self.__dict__
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = datetime.isoformat(self.created_at)
        my_dict['updated_at'] = datetime.isoformat(self.updated_at)
        return my_dict
