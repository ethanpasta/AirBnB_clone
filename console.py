#!/usr/bin/python3
""""Console v 0.0.1"""
import cmd
import sys


class HBNBCommand(cmd.Cmd):
    """Console class"""

    def __init__(self):
        """Console contructor"""
        cmd.Cmd.__init__(self)
        self.prompt = '(hbnb) '

    def emptyline(self):
        """Do nothing when empty line is entered"""

    def do_quit(self, arg=0):
        """Quit command to exit the program"""
        sys.exit(arg)

    def do_EOF(self, line):
        """This method adds EOF handling"""
        return True

    def do_create(self, cls_name=None):
        """Cretaes an instance of @cls_name class"""
        if not cls_name:
            print("** class name missing **")
        else:
            print("create cmd")

    def do_show(self, cls_name=None, id=None):
        """Shows an instance of @cls_name class"""
        if not cls_name:
            print("** class name missing **")
        else:
            print("show cmd")

    def do_destroy(self, cls_name=None, id=None):
        """Deletes an instance of class @cls_name"""
        if not cls_name:
            print("** class name missing **")
        else:
            print("destroy cmd")

    def do_all(self, cls_name=None):
        """Shows all instances of @cls_name class"""
        if not cls_name:
            print("** class name missing **")
        else:
            print("all cmd")

    def do_update(self, cls_name=None, id=None, attr_name=None, attr_val=None):
        """Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)"""
        if not cls_name:
            print("** class name missing **")
        else:
            print("cretae show")

    def postloop(self):
        print(end="")


if __name__ == '__main__':
    cli = HBNBCommand()
    cli.cmdloop()
