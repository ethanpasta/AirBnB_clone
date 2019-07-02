#!/usr/bin/python3
"""Unit tests for console using Mock module from python standard library"""
import unittest
import sys
from console import HBNBCommand
from unittest.mock import create_autospec


class TestConsole_6(unittest.TestCase):

    """Unint tests for console"""

    def setUp(self):
        """Redirecting stdin and stdout"""
        self.mock_stdin = create_autospec(sys.stdin)
        self.mock_stdout = create_autospec(sys.stdout)

    def create(self, server=None):
        """Redirects stdin and stdout to mock module"""
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def _last_write(self, nr=None):
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
        self.assertFalse(cli.onecmd("help"))
        #self.assertTrue(self.mock_stdout.flush.called)
        #print(self._last_write())
