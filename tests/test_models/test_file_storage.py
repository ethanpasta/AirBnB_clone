#!/usr/bin/python3
"""File storage unit tests """
import re
import json
import unittest
import uuid
import os
import pprint
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models import storage


# Changes print to pprint to print in more readable format
pp = pprint.PrettyPrinter(indent=4)
print = pp.pprint


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
        self.assertTrue(all(isinstance(v, BaseModel)
                            for v in dict_obj.values()))

        class_dict = {k.split(".")[1]: k.split(".")[0] for k in dict_obj}
        self.assertTrue(all(issubclass(eval(i), BaseModel)
                            for i in class_dict.values()))
        self.assertTrue(all(uuid.UUID(i).version == 4
                            for i in class_dict))

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
        self.assertTrue(all(isinstance(v, BaseModel)
                            for v in dict_obj.values()))

        class_dict = {k.split(".")[1]: k.split(".")[0] for k in dict_obj}
        self.assertTrue(all(issubclass(eval(i), BaseModel)
                            for i in class_dict.values()))
        self.assertTrue(all(uuid.UUID(i).version == 4
                            for i in class_dict))

    def test_new_method(self):
        """Simple check"""
        my_model = BaseModel()
        my_model.name = "Python"
        d = my_model.to_dict()
        my_other = BaseModel(**d)
        my_other.name = "is cool"
        self.assertTrue(my_model in storage.all().values())
        self.assertFalse(my_other in storage.all().values())

    def test_save_method(self):
        """Checks save method for correct file writing"""
        file = storage._FileStorage__file_path

        my_model = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists(file))

        with open(file, "r") as f:
            json_dict = json.load(f)
        temp_dict = {k: v.to_dict() for k, v in storage.all().items()}
        self.assertEqual(temp_dict, json_dict)

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

    def test_save_basemodel(self):
        """Checks save of the BaseClass"""
        file = storage._FileStorage__file_path
        my_model = BaseModel()
        updated = my_model.__dict__["updated_at"]
        obj = storage.all()["{}.{}".format(my_model.__class__.__name__, my_model.id)]

        self.assertEqual(obj.updated_at, updated)

        self.assertFalse(os.path.exists(file))
        my_model.save()

        self.assertEqual(obj.updated_at, my_model.updated_at)
        self.assertTrue(os.path.exists(file))

    def test_init_and_new(self):
        """Tests init and new. If the arguments is dict,
        then don't call save() of FileStorage"""
        self.assertEqual(storage.all(), {})
        d = {"BaseModel.ee49c413-023a-4b49-bd28-f2936c95460d":
             {"my_number": 89, "__class__": "BaseModel",
              "updated_at": "2017-09-28T21:07:25.047381",
              "created_at": "2017-09-28T21:07:25.047372",
              "name": "Holberton",
              "id": "ee49c413-023a-4b49-bd28-f2936c95460d"}}
        BaseModel(**d)
        self.assertEqual(storage.all(), {})
        BaseModel()
        self.assertTrue(storage.all() != {})
        #print(d)


if __name__ == "__main__":
    unittest.main()
