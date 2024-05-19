#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def default(self, line):
        """Handles unrecognized commands."""
        self.handle_class_syntax(line)

    def handle_class_syntax(self, line):
        """Intercepts commands to check for class.method() syntax."""
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        class_name = match.group(1)
        method_name = match.group(2)
        args = match.group(3)
        match_args = re.search(r'^"([^"]*)"(?:, (.*))?$', args)
        if match_args:
            obj_id = match_args.group(1)
            attr_or_dict = match_args.group(2)
        else:
            obj_id = args
            attr_or_dict = None

        attr_and_val = ""
        if method_name == "update" and attr_or_dict:
            match_dict = re.search(r'^({.*})$', attr_or_dict)
            if match_dict:
                self.update_with_dict(class_name, obj_id, match_dict.group(1))
                return ""
            match_attr_and_val = re.search(r'^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_val:
                attr_and_val = (match_attr_and_val.group(1) or "") + " " + (match_attr_and_val.group(2) or "")
        command = f"{method_name} {class_name} {obj_id} {attr_and_val}"
        self.onecmd(command)
        return command

    def update_with_dict(self, class_name, obj_id, attr_dict):
        """Helper method for update() with a dictionary."""
        dict_str = attr_dict.replace("'", '"')
        attributes = json.loads(dict_str)
        if not class_name:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif obj_id is None:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{obj_id}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                class_attrs = storage.attributes()[class_name]
                for attr, val in attributes.items():
                    if attr in class_attrs:
                        val = class_attrs[attr](val)
                    setattr(storage.all()[key], attr, val)
                storage.all()[key].save()

    def do_EOF(self, line):
        """Handles the end-of-file character to exit the program."""
        print()
        return True

    def do_quit(self, line):
        """Exits the program."""
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
        else:
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
        else:
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
        """Prints string representations of all instances."""
        if line:
            args = line.split()
            if args[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                instances = [str(obj) for key, obj in storage.all().items() if type(obj).__name__ == args[0]]
                print(instances)
        else:
            instances = [str(obj) for key, obj in storage.all().items()]
            print(instances)

    def do_count(self, class_name):
        """Counts the number of instances of a class."""
        if not class_name:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        else:
            count = sum(1 for key in storage.all() if key.startswith(f"{class_name}."))
            print(count)

    def do_update(self, line):
        """Updates an instance by adding or updating an attribute."""
        if not line:
            print("** class name missing **")
            return

        pattern = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:\S+)))?)?)?'
        match = re.search(pattern, line)
        class_name = match.group(1)
        obj_id = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif obj_id is None:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{obj_id}"
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast_type = None
                if not re.search(r'^".*"$', value):
                    if '.' in value:
                        cast_type = float
                    else:
                        cast_type = int
                else:
                    value = value.replace('"', '')
                class_attrs = storage.attributes()[class_name]
                if attribute in class_attrs:
                    value = class_attrs[attribute](value)
                elif cast_type:
                    try:
                        value = cast_type(value)
                    except ValueError:
                        pass  # stay as string if conversion fails
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
