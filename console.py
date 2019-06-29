#!/usr/bin/python3
""""Console v 0.0.1"""
import cmd
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

    def __init__(self):
        """Console contructor"""
        cmd.Cmd.__init__(self)
        self.prompt = '(hbnb) '

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
        Creates a new instance of @cls_name class, and prints the new instance's ID.
        Arguments to enter with command: <class name>
        Example: 'create User'
        """
        if not line:
            print("** class name missing **")
            return
        args = line.split(" ")
        try:
            # args[0] contains class name, create new instance of that class
            obj = eval(args[0])()

            # updates 'updated_at' attribute, and saves into JSON file
            obj.save()

            print(obj.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """
        Prints a string representation of an instance.
        Arguments to enter with command: <class name> <id>
        Example: 'show User 1234-1234-1234'
        """
        if not line:
            print("** class name missing **")
            return
        args = line.split(" ")
        if len(args) < 2:
            print("** instance id missing **")
        else:
            try:
                d = storage.objects
                key = args[0] + '.' + args[1]
                if key in d:
                    print(d[key])
                else:
                    print("** no instance found **")
            except NameError:
                print("** class doesn't exist **")


    def do_destroy(self, line):
        """
        Deletes an instance of a certain class.
        Arguments to enter with command: <class name> <id>
        Example: 'destroy User 1234-1234-1234'
        """
        if not line:
            print("** class name missing **")
            return
        args = line.split(" ")
        if len(args) != 2:
            print("** instance id missing **")
            return
        try:
            d = storage.objects
            key = args[0] + '.' + args[1]
            if key in d:
                del d[key]
                storage.save()
            else:
                print("** no instance found **")
        except NameError:
            print("** class doesn't exist **")

    def do_all(self, line):
        """
        Shows all instances, or instances of a certain class
        Arguments to enter with command (optional): <class name>
        Example: 'all' OR 'all User'
        """
        d = storage.objects
        if not line:
            print([str(x) for x in d.values()])
            return
        names = ["BaseModel", "User", "State", "City", "Amenity",
                 "Place", "Review"]
        args = line.split(" ")
        if args[0] not in names:
            print("** class doesn't exist **")
        else:
            print([str(v) for k, v in d.items() if k.split('.')[0] == args[0]])

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding or
        updating an attribute
        Arguments to enter with command: <class name> <id> <attribute name> "<attribute value>"
        Example: 'update User 1234-1234-1234 my_name "Bob"'
        """
        if not line:
            print("** class name missing **")
            return
        args = line.split(" ")
        l = len(args)
        if l == 1:
            print("** instance id missing **")
        elif l == 2:
            print("** attribute name missing **")
        elif l == 3:
            print("* value missing **")
        else:
            try:
                d = storage.objects
                key = args[0] + '.' + args[1]
                if key in d:
                    setattr(d[key], args[2], args[3][1:-1])
                    storage.save()
                else:
                    print("** no instance found **")
            except NameError:
                print("** class doesn't exist **")

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
        commands = {"all": do_all, "count": my_count, "show": do_show, "destroy": do_destroy, "update": do_update}
        args = line.split(".")
        if len(args) != 2 or args[0] not in names:
            print("*** Unknown syntax: {}".format(line))
            return
        command = args[1]
#        if command == "all()":
#            self.do_all(args[0])
#            return
#        elif command == "count()":
#            count = 0
#            d = storage.all()
#            for obj in d.values():
#                if obj.__class__.__name__ == args[0]:
#                    count += 1
#            print(count)
#            return
#        else:
#            print("*** Unknown syntax: {}".format(line))
#            return

if __name__ == '__main__':
    cli = HBNBCommand()
    cli.cmdloop()
