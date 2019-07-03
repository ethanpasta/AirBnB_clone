#!/usr/bin/python3
"""Base Model unit tests """
import re
import json
import unittest
import uuid
from datetime import datetime
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    """Unit test for Review"""

    def test_basic_test(self):
        """
        Basic tests for Review class
        """
        self.assertTrue(issubclass(Review, BaseModel))
        my_model = Review()
        my_model.name = "Holberton"
        my_model.my_number = 89
        self.assertEqual([my_model.name, my_model.my_number],
                         ["Holberton", 89])

    def test_init(self):
        """
        Test if created_at, updated_at and id are exist
        """
        my_model = Review()
        self.assertTrue(hasattr(my_model, "id"))
        self.assertTrue(hasattr(my_model, "created_at"))
        self.assertTrue(hasattr(my_model, "updated_at"))
        self.assertTrue(hasattr(my_model, "place_id"))
        self.assertTrue(hasattr(my_model, "user_id"))
        self.assertTrue(hasattr(my_model, "text"))

    def test_init_time(self):
        """
        Test if created_at, updated_at are valid
        """
        then = datetime.utcnow()
        my_model = Review()
        now = datetime.utcnow()
        self.assertTrue(then <= my_model.created_at <= now)
        self.assertTrue(then <= my_model.updated_at <= now)
        self.assertTrue(my_model.created_at <= my_model.updated_at)

    def test_init_id(self):
        """
        Test if uuid is valid
        """
        my_model = Review()
        my_model_1 = Review()
        self.assertEqual(uuid.UUID(my_model.id).version, 4)
        self.assertFalse(my_model.id == my_model_1.id)

    def test_str_method(self):
        """
        Tests __str__ of Review class
        """
        my_model = Review()
        s = "[Review] ({}) {}".format(my_model.id, my_model.__dict__)
        self.assertEqual(str(my_model), s)

    def test_save_method(self):
        """
        Tests save() method of BaseClass
        """
        then = datetime.utcnow()
        my_model = Review()
        updated_at = my_model.updated_at
        my_model.save()
        now = datetime.utcnow()
        self.assertTrue(then <= updated_at <= my_model.updated_at)

    def test_to_dict_method(self):
        """
        Tests to_dict() of Review class and check types inside
        """
        my_model = Review()
        my_model.my_number = 777
        d = dict(my_model.__dict__)
        d['__class__'] = "Review"
        d['created_at'] = d['created_at'].isoformat()
        d['updated_at'] = d['updated_at'].isoformat()
        self.assertEqual(d, my_model.to_dict())

        types = [str,
                 "updated_at",
                 "created_at",
                 "__class__",
                 "place_id",
                 "user_id",
                 "text"]
        self.assertTrue(all(isinstance(v, types[0])
                            for k, v in d.items() if k in types[1:]))

        types = [int,
                 "my_number"]
        self.assertTrue(all(isinstance(v, types[0])
                            for k, v in d.items() if k in types[1:]))

    def test_attributes(self):
        """Test attibutes"""
        self.assertEqual(type(Review.place_id), str)
        self.assertEqual(type(Review.user_id), str)
        self.assertEqual(type(Review.text), str)

if __name__ == '__main__':
    unittest.main()
