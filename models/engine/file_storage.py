#!/usr/bin/python3
"""Module file_storage serializes and deserializes JSON types"""
import json
from models.base_model import BaseModel


class FileStorage:
    """Custom Class FileStorage"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Method returns __objects dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """Method sets in __objects the obj with the key <obj class name>.id

        Args:
            obj: the object to write
        """
        FileStorage.__objects[obj.__class__.__name__ + '.' + str(obj.id)] = obj

    def save(self):
        """Method serializes __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, 'w+') as f:
            json.dump(
                {k:v.to_dict() for k,v in FileStorage.__objects.items()}, f)

    def reload(self):
        """Method deserializes the JSON file to __objects (only if the JSON file
        exists; otherwise nothing happens)"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                my_dict = json.loads(f.read())
                FileStorage.__objects = {k:BaseModule(**v) for k,v
                                         in my_dict.items()}
        except Exception:
            pass
