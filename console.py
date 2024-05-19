#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import json
import re

class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """Does nothing on an empty input line."""
        pass

    def do_create(self, class_name):
        """Creates a new instance of a given class."""
        if not class_name:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        else:
            instance = storage.classes()[class_name]()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """Prints the string representation of an instance."""
        if not line:
            print("** class name missing **")
            return

        args = line.split()
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        if not line:
            print("** class name missing **")
            return

        args = line.split()
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances."""
        if line:
            args = line.split()
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                instances = [str(obj) for key, obj in storage.all().items() if type(obj).__name__ == args[0]]
                print(instances)
        else:
            instances = [str(obj) for obj in storage.all().values()]
            print(instances)

    def do_update(self, line):
        """Updates an instance by adding or updating attribute."""
        if not line:
            print("** class name missing **")
            return

        args = line.split()
        if args[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            class_name, obj_id, attr_name, attr_value = args[0], args[1], args[2], args[3].strip('"')
            key = f"{class_name}.{obj_id}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                obj = storage.all()[key]
                if attr_name in storage.attributes()[class_name]:
                    attr_type = storage.attributes()[class_name][attr_name]
                    try:
                        attr_value = attr_type(attr_value)
                    except ValueError:
                        print("** invalid value **")
                        return
                setattr(obj, attr_name, attr_value)
                obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
