#!/usr/bin/python3
""""Console v 0.0.1"""
import cmd
from models.base_model import BaseModel
import models


class HBNBCommand(cmd.Cmd):
    """Console class"""

    def __init__(self):
        """Console contructor"""
        cmd.Cmd.__init__(self)
        self.prompt = '(hbnb) '

    def emptyline(self):
        """Do nothing when empty line is entered"""
        return False

    def do_quit(self, arg=0):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, line):
        """This method adds EOF handling"""
        return True

    def do_create(self, line):
        """Cretaes an instance of @cls_name class"""
        names = ["BaseModel"]
        args = line.split(" ")
        if not line:
            print("** class name missing **")
        elif args[0] not in names:
            print("** class doesn't exist **")
        else:
            obj = BaseModel() # use eval or if statements to create objs for other classes
            obj.save()
            print(obj.id)

    def do_show(self, line):
        """Shows an instance of @cls_name class"""
        names = ["BaseModel"]
        args = line.split(" ")
        l = len(args)
        if not line:
            print("** class name missing **")
        elif args[0] not in names:
            print("** class doesn't exist **")
        elif l == 1:
            print("** instance id missing **")
        else:
            d = models.storage.objects
            key = args[0] + '.' + args[1]
            if key in d:
                print(d[key])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance of class @cls_name"""
        names = ["BaseModel"]
        args = line.split(" ")
        if not line:
            print("** class name missing **")
        elif args[0] not in names:
            print("** class doesn't exist **")
        else:
            d = models.storage.objects
            key = args[0] + '.' + args[1]
            if key in d:
                del d[key]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """Shows all instances of @cls_name class"""
        names = ["BaseModel"]
        args = line.split(" ")
        d = models.storage.objects
        if not line:
            print([str(x) for x in d.values()])
        elif args[0] not in names:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in d.items() if k.split('.')[0] == args[0]])

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)"""
        names = ["BaseModel"]
        args = line.split(" ")
        l = len(args)
        if not line:
            print("** class name missing **")
        elif args[0] not in names:
            print("** class doesn't exist **")
        elif l == 1:
            print("** instance id missing **")
        elif l == 2:
            print("** attribute name missing **")
        elif l == 3:
            print("* value missing **")
        else:
            d = models.storage.objects
            key = args[0] + '.' + args[1]
            if key in d:
                setattr(d[key], args[2], args[3])
                models.storage.save()
            else:
                print("** no instance found **")

if __name__ == '__main__':
    cli = HBNBCommand()
    cli.cmdloop()
