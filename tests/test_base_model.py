#!/usr/bin/python3
"""Base Model unit tests """
import re
import json
import unittest
import uuid
from datetime import datetime
from models.base_model import BaseModel

class TestBaseModel_3(unittest.TestCase):
    """Unit test for BaseModel"""

    def test_basic_test(self):
        """
        Basic tests for BaseModel class
        """
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        self.assertEqual([my_model.name, my_model.my_number],
                         ["Holberton"  , 89])

    def test_init(self):
        """
        Test if created_at, updated_at and id are exist
        """
        my_model = BaseModel()
        self.assertTrue(hasattr(my_model, "id"))
        self.assertTrue(hasattr(my_model, "created_at"))
        self.assertTrue(hasattr(my_model, "updated_at"))

    def test_init_time(self):
        """
        Test if created_at, updated_at are valid
        """
        then = datetime.utcnow()
        my_model = BaseModel()
        now = datetime.utcnow()
        self.assertTrue(then < my_model.created_at < now)
        self.assertTrue(then < my_model.updated_at < now)
        self.assertTrue(my_model.created_at <= my_model.updated_at)

    def test_init_id(self):
        """
        Test if uuid is valid
        """
        my_model = BaseModel()
        my_model_1 = BaseModel()
        self.assertEqual(uuid.UUID(my_model.id).version, 4)
        self.assertFalse(my_model.id == my_model_1.id)

    def test_str_method(self):
        """
        Tests __str__ of BaseModel class
        """
        my_model = BaseModel()
        s = "[BaseModel] ({}) {}".format(my_model.id, my_model.__dict__)
        self.assertEqual(str(my_model), s)

    def test_save_method(self):
        """
        Tests save() method of BaseClass
        """
        then = datetime.utcnow()
        my_model = BaseModel()
        updated_at = my_model.updated_at
        my_model.save()
        now = datetime.utcnow()
        self.assertTrue(then < updated_at < my_model.updated_at < now)

    def test_to_dict_method(self):
        """
        Tests to_dict() of BaseModel class and check types inside
        """
        my_model = BaseModel()
        my_model.my_number = 777
        d = dict(my_model.__dict__)
        d['__class__'] = "BaseModel"
        d['created_at'] = d['created_at'].isoformat()
        d['updated_at'] = d['updated_at'].isoformat()
        self.assertEqual(d, my_model.to_dict())

        types = [str,
                 "updated_at",
                 "cretaed_at",
                 "__class__",
                 "id"]
        self.assertTrue(all(type(v) == types[0]
                            for k, v in d.items() if k in types[1:]))

        types = [int,
                 "my_number"]
        self.assertTrue(all(type(v) == types[0]
                            for k, v in d.items() if k in types[1:]))


class TestBaseModel_4(unittest.TestCase):
    """
    Test @kwargs argument for BaseModel constructor
    """

    def test_dict(self):
        """
        Basic test of init method
        """
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertTrue(type(my_new_model.created_at) == datetime)
        self.assertTrue(type(my_new_model.updated_at) == datetime)
        self.assertFalse(my_model is my_new_model)
        self.assertEqual(my_new_model.to_dict(), my_model_json)

    # def test_dict_check_types(self):
    #     """
    #     Test the type of updated_at and created_at
    #     """
    #     my_model = BaseModel()
    #     my_model.name = "Holberton"
    #     my_model.my_number = 89
    #     my_model_json = my_model.to_dict()
    #     my_new_model = BaseModel(**my_model_json)
    #     self.assertTrue(type(my_new_model.created_at) == datetime)
    #     self.assertFalse(my_model is my_new_model)
    #     self.assertEqual(my_new_model.to_dict(), my_model_json)
