#!/usr/bin/python3
"""File storage unit tests
"""
import re
import json
import unittest
import uuid
import os
import pprint
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.file_storage import FileStorage


class TestFileStorage_5(unittest.TestCase):

    """Test storage engine which uses JSON to store objects.
     Simple implementation of objects persistence"""

    def setUp(self):
        """
        Remove file and do additional set up
        """
        file = storage._FileStorage__file_path
        storage._FileStorage__objects = {}
        if (os.path.exists(file)):
            os.remove(file)

    def test_private_attributes(self):
        """Test private attributes"""
        with self.assertRaises(AttributeError):
            print(storage.objects)
        with self.assertRaises(AttributeError):
            print(storage.file_path)

    def test_simple_check(self):
        """Simple check"""
        file = storage._FileStorage__file_path
        self.assertTrue(type(file) == str)

        obj1 = BaseModel()
        obj2 = BaseModel()
        obj3 = BaseModel()
        obj4 = BaseModel()
        obj5 = BaseModel()

        dict_obj = storage._FileStorage__objects
        self.assertTrue(type(dict_obj) == dict)
        self.assertTrue(all(type(v) == BaseModel)
                        for v in dict_obj.values())

    def test_all_method(self):
        """Checks whether all returning dict of objects"""
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj3 = BaseModel()
        obj4 = BaseModel()
        obj5 = BaseModel()

        dict_obj = storage.all()
        self.assertEqual(dict_obj, storage._FileStorage__objects)
        self.assertTrue(type(dict_obj) == dict)
        self.assertTrue(all(type(v) == BaseModel)
                        for v in dict_obj.values())

    def test_new_method(self):
        """Simple check"""
        my_model = BaseModel()
        my_model.name = "Python"
        d = my_model.to_dict()
        my_other = BaseModel(**d)
        my_other.name = "is cool"
        self.assertTrue(my_model in storage.all().values())
        self.assertFalse(my_other in storage.all().values())

    def test_reload_method(self):
        """Checks reload method for correct deserialization"""
        file = storage._FileStorage__file_path
        self.assertFalse(os.path.exists(file))

        storage.reload()  # file does not exists
        self.assertFalse(storage.all())
        my_model = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists(file))

        with open(file, "r") as f:
            json_dict = json.load(f)
        temp_dict = {k: v.to_dict() for k, v in storage.all().items()}
        self.assertEqual(temp_dict, json_dict)

    def test_reload_method_1(self):
        """Test reload method"""
        file = FileStorage()
        my_model = BaseModel()
        key = "BaseModel" + "." + my_model.id
        file.new(my_model)
        file.save()
        file.reload()
        self.assertTrue(file.all()[key] is not None)

        with self.assertRaises(KeyError):
            storage.all()["Non existent key"]

    def test_reload_method_2(self):
        """Test reload method"""
        obj = BaseModel()
        storage.save()
        with open("file.json", "r") as f:
            json_dict = json.load(f)
        self.assertIn(obj.to_dict(), json_dict.values())

    def test_reload_method_3(self):
        """Reload test"""
        fs = FileStorage()
        b = BaseModel()
        key = "BaseModel" + '.' + b.id
        fs.new(b)
        fs.save()
        fs._FileStorage__objects = {}
        fs.reload()
        self.assertTrue(fs.all()[key])

    def test_save(self):
        """Tests save method"""
        obj = BaseModel()
        upd = obj.updated_at
        obj.save()
        self.assertTrue(upd != obj.updated_at)

        self.assertTrue(os.path.exists("file.json"))

if __name__ == "__main__":
    unittest.main()
