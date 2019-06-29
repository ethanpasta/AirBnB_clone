#!/usr/bin/python3
"""User class:
     Class which inherits from BaseModel
"""
from models.base_model import BaseModel


class User(BaseModel):
    """User class for AirBnB project"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self):
        """Initialization method for User class"""
        BaseModel.__init__(self)
