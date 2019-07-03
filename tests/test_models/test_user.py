#!/usr/bin/python3
"""Base Model unit tests """
import re
import json
import unittest
import uuid
from datetime import datetime
from models.user import User
from models.base_model import BaseModel


class TestUser_8(unittest.TestCase):

    """Unit test for User"""

    def test_attributes_email(self):
        """Test attibutes"""
        self.assertEqual(type(User.email), str)
        self.assertEqual(type(User.password), str)
        self.assertEqual(type(User.first_name), str)
        self.assertEqual(type(User.last_name), str)

if __name__ == "__main__":
    unittest.main()
