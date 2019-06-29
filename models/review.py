#!/usr/bin/python3
"""Module for Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Custom Review class that inherits the BaseModel class"""
    place_id = ""
    user_id = ""
    text = ""
