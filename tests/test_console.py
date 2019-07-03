#!/usr/bin/python3
"""Unit tests for console using Mock module from python standard library"""
import unittest
import os
import sys
import pprint
from console import HBNBCommand
from models import storage
from unittest.mock import create_autospec
from unittest.mock import patch
from io import StringIO

# Pretty print, redifined print
pp = pprint.PrettyPrinter(indent=4)
pp = pp.pprint


class TestConsole_6(unittest.TestCase):

    """Unint tests for console"""

    err = ["** class name missing **",
           "** class doesn't exist **",
           "** instance id missing **",
           "** no instance found **",
           ""]

    cls = ["BaseModel",
           "User",
           "State",
           "City",
           "Place",
           "Amenity",
           "Review"]

    def setUp(self):
        """Redirecting stdin and stdout"""
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create(self, server=None):
        """Redirects stdin and stdout to mock module"""
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def last_write(self, nr=None):
        """Returns last `n` output lines"""
        if nr is None:
            return self.mock_stdout.write.call_args[0][0]
        return "".join(map(lambda c: c[0][0],
                           self.mock_stdout.write.call_args_list[-nr:]))

    def test_quit(self):
        """Quit command"""
        cli = self.create()
        self.assertTrue(cli.onecmd("quit"))

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

    def test_empty_line(self):
        """Tests empty line"""
        cli = self.create()
        self.assertFalse(cli.onecmd("help"))
        ss = self.last_write(10)
        self.assertFalse(cli.onecmd(""))
        s = self.last_write(10)
        self.assertEqual(ss, s)

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
