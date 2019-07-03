#!/usr/bin/python3
""""Console v 0.0.1"""
import cmd
import json
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):

    """Console class"""

    prompt = '(hbnb) '

    def my_errors(self, line, num_args):
        """Method displays different error messages"""
        classes = ["BaseModel", "User", "State", "City", "Amenity",
                   "Place", "Review"]
        msg = [
            "** class name missing **",
            "** class doesn't exist **",
            "** instance id missing **",
            "** no instance found **",
            "** attribute name missing **",
            "** value missing **"]
        if not line:
            print(msg[0])
            return 1
        args = line.split()
        if num_args >= 1 and args[0] not in classes:
            print(msg[1])
            return 1
        elif num_args == 1:
            return 0
        if num_args >= 2 and len(args) < 2:
            print(msg[2])
            return 1
        d = storage.all()
        for i in range(len(args)):
            if args[i][0] == '"':
                args[i] = args[i].replace('"', "")
        key = args[0] + '.' + args[1]
        if num_args >= 2 and key not in d:
            print(msg[3])
            return 1
        elif num_args == 2:
            return 0
        if num_args >= 4 and len(args) < 3:
            print(msg[4])
            return 1
        if num_args >= 4 and len(args) < 4:
            print(msg[5])
            return 1
        return 0

    def emptyline(self):
        """Do nothing when empty line is entered"""
        return False

    def do_quit(self, line):
        """
        Quit command interpreter with 'quit'
        """
        return True

    def do_EOF(self, line):
        """
        Quit command interpreter with ctrl+d
        """
        return True

    def do_create(self, line):
        """
        Creates a new instance of @cls_name class,
        and prints the new instance's ID.
        Arguments to enter with command: <class name>
        Example: 'create User'
        """
        if (self.my_errors(line, 1) == 1):
            return
        args = line.split(" ")
        # args[0] contains class name, create new instance of that class
        obj = eval(args[0])()

        # updates 'updated_at' attribute, and saves into JSON file
        obj.save()

        print(obj.id)

    def do_show(self, line):
        """
        Prints a string representation of an instance.
        Arguments to enter with command: <class name> <id>
        Example: 'show User 1234-1234-1234'
        """

        if (self.my_errors(line, 2) == 1):
            return
        args = line.split()
        d = storage.all()
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        print(d[key])

    def do_destroy(self, line):
        """
        Deletes an instance of a certain class.
        Arguments to enter with command: <class name> <id>
        Example: 'destroy User 1234-1234-1234'
        """
        if (self.my_errors(line, 2) == 1):
            return
        args = line.split()
        d = storage.all()
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        del d[key]
        storage.save()

    def do_all(self, line):
        """
        Shows all instances, or instances of a certain class
        Arguments to enter with command (optional): <class name>
        Example: 'all' OR 'all User'
        """
        d = storage.all()
        if not line:
            print([str(x) for x in d.values()])
            return
        args = line.split()
        if (self.my_errors(line, 1) == 1):
            return
        print([str(v) for v in d.values() if v.__class__.__name__ == args[0]])

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating an attribute
        Arguments to enter with command:
        <class name> <id> <attribute name> "<attribute value>"
        Example: 'update User 1234-1234-1234 my_name "Bob"'
        """
        if (self.my_errors(line, 4) == 1):
            return
        args = line.split()
        d = storage.all()
        for i in range(len(args[1:]) + 1):
            if args[i][0] == '"':
                args[i] = args[i].replace('"', "")
        key = args[0] + '.' + args[1]
        attr_k = args[2]
        attr_v = args[3]
        class_attr = type(d[key]).__dict__
        if attr_k in class_attr.keys():
            try:
                attr_v = type(class_attr[attr_k])(attr_v)
            except Exception:
                print("Entered wrong value type")
                return
        setattr(d[key], attr_k, attr_v)
        storage.save()

    def my_count(self, class_n):
        """Method counts instances of a certain class"""
        c = 0
        for o in storage.all().values():
            if o.__class__.__name__ == class_n:
                c += 1
        print(c)

    def default(self, line):
        """Method to take care of following commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation)
        """
        names = ["BaseModel", "User", "State", "City", "Amenity",
                 "Place", "Review"]
        commands = {"all": self.do_all,
                    "count": self.my_count,
                    "show": self.do_show,
                    "destroy": self.do_destroy,
                    "update": self.do_update}
        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in names \
           or args[1] not in commands.keys():
            super().default(line)
            return
        if args[1] in ["all", "count"]:
            commands[args[1]](args[0])
        elif args[1] in ["show", "destroy"]:
            commands[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            a = args[2].split(", {")
            if len(a) > 1:
                b = '{' + a[1]
                c = b.split(":", 1)
                c[0] = c[0].replace("\'", "\"") + ":"
                d = json.loads(''.join(c))
                for k, v in d.items():
                    cmd = str(args[1]) + " " + str(args[0]) + " " \
                           + str(a[0]) + " " + str(k) + " " + str(v)
                    # r = self.onecmd(cmd)
                    r = commands[args[1]](str(args[0]) + " " \
                           + str(a[0]) + " " + str(k) + " " + str(v))
                    if not r:
                        break
            else:
                rest = args[2].split(", ")
                commands[args[1]](args[0] + " " + rest[0] + " " +
                                  rest[1] + " " + rest[2])

    def do_mymy(self, line):
        """Onecmd"""
        self.onecmd(line)

if __name__ == '__main__':
    cli = HBNBCommand()
    cli.cmdloop()
