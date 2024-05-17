#0x00. AirBnB clone - The console  Project

##Description of The project
This is the first part of the AirBNB clone  project. In this part my partner and I worked on the backend part of the project and later on interfaced it with the console application using the python cmd module.

The python objects we generated are stored in the json file and can be accessed using the json module in python.

##Description of the command interpreter.
The command line interpreter operates just like the Bash shell but is specifically designed for the AirBnB website.
Some of the most commonly used commands are count, create, update, destroy. These commands can be used to perform functions like creating new objects, retrieving objects,updating attributes and destroying objects.

## How to start it.
The steps below are used to get the project running in yor local machine for the purposes of developing and testing.

##installation.
Clone the project repo from Github. The repo contains the shell program and its dependencies.
Once done cloning, you'll find various files including console.py(the main excutable file of the project), file_storage.py(python class that serializes instances to a json file and deserializes Json file to instnces), init.py(unique storage for the application), base_model.py(defines all common attributes for other classes), user.py(the class inherits from base_model), state.py(states the classes that inherit from the basee_model), city.py(the city class), amenity.py(amenity class), place.py(place class), and review.py(Review class)

##Usage
The airBnB application  can work in interactive and Non-Interactive modes.
In the Interactive mode, the console displays a hbnb prompt that allows the user to write and execute a command. The prompt appears again after the user runs a prompt and awaits a new command from the user.

On the other side, the No interactive mode pipes commmands into the shell's execution.There are no prompts in this mode and commands are directly excuted upon starting the shell. 
Example:
'''
$ echo "create Place" | ./console.py
(hbnb)
e37ebcd3-f8e1-4c1f-8095-7a019070b1fa
(hbnb)
'''

## Command Input format
In case of the Interactive mode, the commands are written using a keyboard and excuted using the Enter Key. Once the command is  not excuted successfully, an error message is displayed and the console can be exited by typing the **quit** command or using key  combinations of **CTRL + C** or **EOF** command 

In the Non Interactive mode, the commands are piped through an echo as shown in the exapmle above.

##Some commands and what they do.
**quit or EOF**: Exits the program.
**help**: Provides instructions on using a command.
**create**: Creates a new instance of a valid class and saves it to the JSON file.
**show**: Prints the string representation of an instance based on the class name and ID.
**destroy**: Deletes an instance based on the class name and ID.
**all**: Prints string representations of all instances based on the class name.
**update**: Updates an instance based on the class name and ID by adding or updating attributes.
**count**: Retrieves the number of instances of a class.
