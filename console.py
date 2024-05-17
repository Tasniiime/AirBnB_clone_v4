#!/usr/bin/python3
"""Module for the entry point of the command interpreter."""

import cmd
import json
import re
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command interpreter class for the AirBnB clone."""

    prompt = "(hbnb) "

    def default(self, line):
        """Handle unrecognized commands."""
        self._parse_class_syntax(line)

    def _parse_class_syntax(self, line):
        """Parse and execute commands of the form ClassName.method(args)"""
        pattern = r"^(\w+)\.(\w+)\(([^)]*)\)$"
        match = re.match(pattern, line)
        if not match:
            return line
        cls_name, method, args = match.groups()
        args = args.split(", ", 1)
        uid = args[0].strip('"')
        attr_or_dict = args[1] if len(args) > 1 else None

        if method == "update" and attr_or_dict:
            if re.match(r'^{.*}$', attr_or_dict):
                self._update_with_dict(cls_name, uid, attr_or_dict)
            else:
                attr, value = re.split(r'"\s*,\s*', attr_or_dict)
                self.onecmd(
                    f'{method} {cls_name} {uid} {attr.strip()} {value.strip()}'
                )
        else:
            self.onecmd(f'{method} {cls_name} {uid}')

    def _update_with_dict(self, cls_name, uid, s_dict):
        """Update instance attributes using a dictionary."""
        try:
            updates = json.loads(s_dict.replace("'", '"'))
        except json.JSONDecodeError:
            return

        if cls_name not in storage.classes():
            print("** class doesn't exist **")
            return

        key = f"{cls_name}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return

        obj = storage.all()[key]
        for attr, val in updates.items():
            if attr in storage.attributes()[cls_name]:
                val = storage.attributes()[cls_name][attr](val)
            setattr(obj, attr, val)
        obj.save()

    def do_EOF(self, line):
        """Exit the command interpreter on EOF character (Ctrl+D)."""
        print()
        return True

    def do_quit(self, line):
        """Exit the command interpreter."""
        return True

    def emptyline(self):
        """Do nothing on empty input line."""
        pass

    def do_create(self, line):
        """Create a new instance of a specified class."""
        if not line:
            print("** class name missing **")
            return
        if line not in storage.classes():
            print("** class doesn't exist **")
            return
        instance = storage.classes()[line]()
        instance.save()
        print(instance.id)

    def do_show(self, line):
        """Display the string representation of an instance."""
        if not line:
            print("** class name missing **")
            return
        parts = line.split()
        if len(parts) < 2:
            print("** instance id missing **")
            return
        cls_name, uid = parts
        if cls_name not in storage.classes():
            print("** class doesn't exist **")
            return
        key = f"{cls_name}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, line):
        """Delete an instance based on class name and ID."""
        if not line:
            print("** class name missing **")
            return
        parts = line.split()
        if len(parts) < 2:
            print("** instance id missing **")
            return
        cls_name, uid = parts
        if cls_name not in storage.classes():
            print("** class doesn't exist **")
            return
        key = f"{cls_name}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, line):
        """Display all instances or all instances of a specific class."""
        if line:
            if line not in storage.classes():
                print("** class doesn't exist **")
                return
            print([str(obj) for obj in storage.all().values()
                   if isinstance(obj, storage.classes()[line])])
        else:
            print([str(obj) for obj in storage.all().values()])

    def do_count(self, line):
        """Count the number of instances of a class."""
        if not line:
            print("** class name missing **")
            return
        if line not in storage.classes():
            print("** class doesn't exist **")
            return
        count = sum(1 for obj in storage.all().values()
                    if isinstance(obj, storage.classes()[line]))
        print(count)

    def do_update(self, line):
        """Update an instance by adding or updating an attribute."""
        parts = line.split(maxsplit=3)
        if len(parts) < 1:
            print("** class name missing **")
            return
        cls_name = parts[0]
        if cls_name not in storage.classes():
            print("** class doesn't exist **")
            return
        if len(parts) < 2:
            print("** instance id missing **")
            return
        uid = parts[1]
        key = f"{cls_name}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(parts) < 3:
            print("** attribute name missing **")
            return
        attr_name = parts[2]
        if len(parts) < 4:
            print("** value missing **")
            return
        value = parts[3].strip('"')
        obj = storage.all()[key]
        cast_type = storage.attributes()[cls_name].get(attr_name, str)
        try:
            value = cast_type(value)
        except ValueError:
            pass
        setattr(obj, attr_name, value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
