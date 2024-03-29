#!/usr/bin/python3
"""Base Model unit tests """
import re
import json
import unittest
import uuid
from datetime import datetime
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):

    """Unit test for Place"""

    def test_basic_test(self):
        """
        Basic tests for Place class
        """
        self.assertTrue(issubclass(Place, BaseModel))
        my_model = Place()
        my_model.name = "Holberton"
        my_model.my_number = 89
        self.assertEqual([my_model.name, my_model.my_number],
                         ["Holberton", 89])

    def test_init(self):
        """
        Test if created_at, updated_at and id are exist
        """
        my_model = Place()
        self.assertTrue(hasattr(my_model, "id"))
        self.assertTrue(hasattr(my_model, "created_at"))
        self.assertTrue(hasattr(my_model, "updated_at"))

        self.assertTrue(hasattr(my_model, "city_id"))
        self.assertTrue(hasattr(my_model, "user_id"))
        self.assertTrue(hasattr(my_model, "name"))
        self.assertTrue(hasattr(my_model, "description"))
        self.assertTrue(hasattr(my_model, "number_rooms"))
        self.assertTrue(hasattr(my_model, "number_bathrooms"))
        self.assertTrue(hasattr(my_model, "max_guest"))
        self.assertTrue(hasattr(my_model, "price_by_night"))

        self.assertTrue(hasattr(my_model, "latitude"))
        self.assertTrue(hasattr(my_model, "longitude"))
        self.assertTrue(hasattr(my_model, "amenity_ids"))

    def test_init_time(self):
        """
        Test if created_at, updated_at are valid
        """
        then = datetime.utcnow()
        my_model = Place()
        now = datetime.utcnow()
        self.assertTrue(then <= my_model.created_at <= now)
        self.assertTrue(then <= my_model.updated_at <= now)
        self.assertTrue(my_model.created_at <= my_model.updated_at)

    def test_init_id(self):
        """
        Test if uuid is valid
        """
        my_model = Place()
        my_model_1 = Place()
        self.assertEqual(uuid.UUID(my_model.id).version, 4)
        self.assertFalse(my_model.id == my_model_1.id)

    def test_str_method(self):
        """
        Tests __str__ of Place class
        """
        my_model = Place()
        s = "[Place] ({}) {}".format(my_model.id, my_model.__dict__)
        self.assertEqual(str(my_model), s)

    def test_save_method(self):
        """
        Tests save() method of BaseClass
        """
        then = datetime.utcnow()
        my_model = Place()
        updated_at = my_model.updated_at
        my_model.save()
        now = datetime.utcnow()
        self.assertTrue(then <= updated_at <= my_model.updated_at)

    def test_to_dict_method(self):
        """
        Tests to_dict() of Place class and check types inside
        """
        my_model = Place()
        my_model.my_number = 777
        d = dict(my_model.__dict__)
        d['__class__'] = "Place"
        d['created_at'] = d['created_at'].isoformat()
        d['updated_at'] = d['updated_at'].isoformat()
        self.assertEqual(d, my_model.to_dict())

        types = [str,
                 "updated_at",
                 "created_at",
                 "__class__",
                 "id",
                 "city_id",
                 "user_id",
                 "name",
                 "description",
                 "amenity_ids"]
        self.assertTrue(all(isinstance(v, types[0])
                            for k, v in d.items() if k in types[1:]))

        types = [int,
                 "my_number",
                 "number_rooms",
                 "number_bathrooms",
                 "max_guest",
                 "price_by_night"]
        self.assertTrue(all(isinstance(v, types[0])
                            for k, v in d.items() if k in types[1:]))

        types = [float,
                 "latitude",
                 "longitude"]
        self.assertTrue(all(isinstance(v, types[0])
                            for k, v in d.items() if k in types[1:]))

    def test_attributes(self):
        """Test attibutes"""
        self.assertEqual(type(Place.city_id), str)
        self.assertEqual(type(Place.user_id), str)
        self.assertEqual(type(Place.name), str)
        self.assertEqual(type(Place.description), str)

        self.assertEqual(type(Place.number_rooms), int)
        self.assertEqual(type(Place.number_bathrooms), int)
        self.assertEqual(type(Place.max_guest), int)
        self.assertEqual(type(Place.price_by_night), int)

        self.assertEqual(type(Place.latitude), float)
        self.assertEqual(type(Place.longitude), float)
        self.assertEqual(type(Place.amenity_ids), list)

if __name__ == '__main__':
    unittest.main()
