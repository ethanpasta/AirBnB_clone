#!/usr/bin/python3
"""Base model class:
   This class is base class for all other class of AirBnB project"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Base model class"""

    id = uuid4()
    created_at = datetime.utcnow()
    updated_at = created_at

    def __str__(self):
        """Str method for Base class"""
        return "[{}] ({}) {}".format("BaseModel", self.id, self.__dict__)

    def save(self):
        """updates the public instance attribute
        updated_at with the current datetime"""
        
        
