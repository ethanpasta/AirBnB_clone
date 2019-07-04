#!/usr/bin/python3
"""Unit tests for console using Mock module from python standard library
   Checks console capturing stdout into a StringIO object
"""
import os
import sys
import unittest
from unittest.mock import create_autospec, patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestConsole_6(unittest.TestCase):
    """Unint tests for console"""

    def setUp(self):
        """Redirecting stdin and stdout"""
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)
        self.err = ["** class name missing **",
                    "** class doesn't exist **",
                    "** instance id missing **",
                    "** no instance found **",
                    ]

        self.cls = ["BaseModel",
                    "User",
                    "State",
                    "City",
                    "Place",
                    "Amenity",
                    "Review"]

    def create(self, server=None):
        """Redirects stdin and stdout to the mock module"""
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def last_write(self, nr=None):
        """Returns last n output lines"""
        if nr is None:
            return self.mock_stdout.write.call_args[0][0]
        return "".join(map(lambda c: c[0][0],
                           self.mock_stdout.write.call_args_list[-nr:]))

    def test_quit(self):
        """Quit command"""
        cli = self.create()
        self.assertTrue(cli.onecmd("quit"))

    def test_quit(self):
        """EOF command"""
        cli = self.create()
        self.assertTrue(cli.onecmd("EOF"))

    def test_help(self):
        """Test help command"""
        cli = self.create()
        self.assertEqual(cli.prompt, "(hbnb) ")
        self.assertFalse(cli.onecmd("help"))
        s = self.last_write(10)
        commands = ["EOF",
                    "all",
                    "create",
                    "destroy",
                    "help",
                    "quit",
                    "show",
                    "update"]
        for i in commands:
            self.assertTrue(i in s)

        msg = []
        for i in commands:
            self.assertFalse(cli.onecmd("help {}".format(i)))
            s = self.last_write(10)
            msg.append(s.split("update")[1].strip())
            self.assertTrue(s)

    def test_empty_line(self):
        """Tests empty line"""
        cli = self.create()
        self.assertFalse(cli.onecmd("\n"))
        s = self.last_write(10)
        self.assertFalse(s)

        self.assertFalse(cli.onecmd(""))
        s = self.last_write(10)
        self.assertFalse(s)

    def test_create(self):
        """Tests create"""
        cli = self.create()
        # Test unknown class
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd("create Bae"))
        self.assertEqual(self.err[1], fakeOutput.getvalue().strip())

        # Test without args
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd("create"))
        self.assertEqual(self.err[0], fakeOutput.getvalue().strip())

        # Test with classes
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("create {}".format(i)))
            with open("file.json", "r") as f:
                file = f.read()
            self.assertIn(fakeOutput.getvalue().strip(), file)

    def test_show(self):
        """Tests show"""
        cli = self.create()
        # Test unknown class
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd("show MyClass"))
        self.assertEqual(self.err[1], fakeOutput.getvalue().strip())

        # Test without args
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd("show"))
        self.assertEqual(self.err[0], fakeOutput.getvalue().strip())

        # Test without ID
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("show {}".format(i)))
            self.assertEqual(fakeOutput.getvalue().strip(), self.err[2])

        # Test no instance found
        uid = "437ae424409acc0f564-4cdff"
        storage._FileStorage__objects = {}
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("show {} {}".format(i, uid)))
            self.assertEqual(fakeOutput.getvalue().strip(), self.err[3])

        # Test show
        ids = []  # Generate ids for testing
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("create {}".format(i)))
            ids.append(fakeOutput.getvalue().strip())

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("show {} {}".format(e, ids[i])))
                key = e + "." + ids[i]
            self.assertEqual(fakeOutput.getvalue().strip(),
                             str(storage.all()[key]))

    def test_destroy(self):
        """Test destroy"""
        cli = self.create()
        # Test unknown class
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd("destroy MyClass"))
        self.assertEqual(self.err[1], fakeOutput.getvalue().strip())

        # Test without args
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd("destroy"))
        self.assertEqual(self.err[0], fakeOutput.getvalue().strip())

        # Test without ID
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("destroy {}".format(i)))
            self.assertEqual(fakeOutput.getvalue().strip(), self.err[2])

        # Test no instance found
        uid = "437ae424409acc0f564-4cdff"
        storage._FileStorage__objects = {}
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("destroy {} {}".format(i, uid)))
            self.assertEqual(fakeOutput.getvalue().strip(), self.err[3])

        # Test destroy functionality
        ids = []
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("create {}".format(i)))
            ids.append(fakeOutput.getvalue().strip())

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("destroy {} {}".format(e, ids[i])))
                key = e + "." + ids[i]
            self.assertFalse(key in storage.all())

    def test_all(self):
        """Test all, two syntaxes"""
        if os.path.exists("file.json"):
            os.remove("file.json")
        storage._FileStorage__objects = {}

        base = [BaseModel(), BaseModel()]
        user = [User(), User()]
        state = [State(), State()]
        city = [City(), City()]
        place = [Place(), Place()]
        amenity = [Amenity(), Amenity()]
        review = [Review(), Review()]

        classes = {"BaseModel": base,
                   "User": user,
                   "State": state,
                   "City": city,
                   "Place": place,
                   "Amenity": amenity,
                   "Review": review}

        storage.save()
        cli = self.create()

        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.all()".format(i)))
            l = eval(fakeOutput.getvalue().strip())
            self.assertEqual(len(l), 2)
            self.assertIn(str(classes[i][0]), l)
            self.assertIn(str(classes[i][1]), l)

    def test_count(self):
        """Test count, which gives 7 GREEN checks"""
        if os.path.exists("file.json"):
            os.remove("file.json")
        storage._FileStorage__objects = {}
        base = BaseModel()
        user = User()
        state = State()
        city = City()
        place = Place()
        amenity = Amenity()
        review = Review()

        base2 = BaseModel()
        user2 = User()
        state2 = State()
        city2 = City()
        place2 = Place()
        amenity2 = Amenity()
        review2 = Review()

        storage.save()
        cli = self.create()

        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.count()".format(i)))
            self.assertEqual(fakeOutput.getvalue(), "2\n")

    def test_show_advanced(self):
        """Tests show"""
        cli = self.create()
        # Test without ID
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.show()".format(i)))
            self.assertEqual(fakeOutput.getvalue().strip(), self.err[2])

        # Test no instance found
        uid = "437ae424409acc0f564-4cdff"
        storage._FileStorage__objects = {}
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.show({})".format(i, uid)))
            self.assertEqual(fakeOutput.getvalue().strip(), self.err[3])

        # Test show
        ids = []  # Generate ids for testing
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("create {}".format(i)))
            ids.append(fakeOutput.getvalue().strip())

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.show({})".format(e, ids[i])))
                key = e + "." + ids[i]
            self.assertEqual(fakeOutput.getvalue().strip(),
                             str(storage.all()[key]))

    def test_destroy_advanced(self):
        """Test destroy"""
        cli = self.create()

        # Test no instance found
        uid = "437ae424409acc0f564-4cdff"
        storage._FileStorage__objects = {}
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.destroy({})".format(i, uid)))
            self.assertEqual(fakeOutput.getvalue().strip(), self.err[3])

        # Test destroy functionality
        ids = []
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("create {}".format(i)))
            ids.append(fakeOutput.getvalue().strip())

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.destroy({})"
                                            .format(e, ids[i])))
                key = e + "." + ids[i]
            self.assertFalse(key in storage.all())

    def test_update(self):
        """Tests show"""
        cli = self.create()

        # Test show
        ids = []  # Generate ids for testing
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("create {}".format(i)))
            ids.append(fakeOutput.getvalue().strip())

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd(
                    '{}.update("{}", "first_name", "John")'.format(e, ids[i])))

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.show({})".format(e, ids[i])))
            self.assertTrue("'first_name': 'John'"
                            in fakeOutput.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd("create BaseModel"))
        ids = fakeOutput.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.assertFalse(cli.onecmd(
                'update BaseModel {} first_name "John"'.format(ids)))

        key = "BaseModel" + "." + ids
        self.assertEqual(storage.all()[key].first_name, "John")

    def test_update_dictionary(self):
        """Tests dictionary update"""
        cli = self.create()

        # Test show
        ids = []  # Generate ids for testing
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("create {}".format(i)))
            ids.append(fakeOutput.getvalue().strip())

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd(
                    '{}.update("{}", {{"first_name": "John", "age": 89}})'
                    .format(e, ids[i])))

        for i, e in enumerate(self.cls):
            with patch('sys.stdout', new=StringIO()) as fakeOutput:
                self.assertFalse(cli.onecmd("{}.show({})".format(e, ids[i])))
            self.assertTrue("'first_name': 'John'"
                            in fakeOutput.getvalue().strip())
            self.assertTrue("'age': 89"
                            in fakeOutput.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
