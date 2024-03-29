# AirBnB Clone - The Holberton B&B

![Image of hbnb](https://github.com/ethanpasta/AirBnB_clone/blob/Dev/65f4a1dd9c51265f49d0.png)

## Description

This is the final 4 month project at Holberton School San Francisco. The goal of the project is to deploy a simple copy of the AirBnB website - hBnB. The web application will be composed by:

- A command interpreter to manipulate data without a visual interface, like a shell (for development and debugging)
- A website (front-end) that show the final product to everyone: static and dynamic
- A database or files that store data
- An API that provides a communication interface between the front-end and your data (retrieve, create, delete and update them)
---

## Final Product

![Image of hbnb](https://github.com/ethanpasta/AirBnB_clone/blob/master/100-index.png)

## Step 1: The Console

* Create a data model
* Manage (create, update, destroy, etc) objects via a console/command interpreter
* Store and persist objects to files (JSON files)

The first step is to manipulate a powerful storage system. This storage engine will give an abstraction between objects and how they are stored and persisted. 

![Image of hbnb](https://github.com/ethanpasta/AirBnB_clone/blob/master/815046647d23428a14ca.png)

## Commands

|                          Commands                          |                                                        Description                                                       |
|:----------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------------------:|
|                           `quit`                           |                                                     Quits the console                                                    |
|                          `Ctrl+D`                          |                                                     Quits the console                                                    |
|                 `help` or `help <command>`                 |                           Displays all commands or Displays instructions for a specific command                          |
|                      `create <class>`                      |                   Creates an object of type <class>, saves it to a JSON file, and prints the objects ID                  |
|                     `show <class> <ID>`                    |                                         Shows string representation of an object                                         |
|                   `destroy <class> <ID>`                   |                                                    Deletes an objects                                                    |
|                   `all` or `all <class>`                   | Prints all string representations of all objects or Prints all string representations of all objects of a specific class |
| `update <class> <id> <attribute name> "<attribute value>"` |                               Updates an object with a certain attribute (new or existing)                               |
|                       `<class>.all()`                      |                                                   Same as `all <class>`                                                  |
|                      `<class>.count()`                     |                                    Retrieves the number of objects of a certain class                                    |
|                    `<class>.show(<ID>)`                    |                                                Same as `show <class> <ID>`                                               |
|                   `<class>.destroy(<ID>)`                  |                                              Same as `destroy <class> <ID>`                                              |
| `<class>.update(<ID>, <attribute name>, <attribute value>` |                             Same as `update <class> <ID> <attribute name> <attribute value>`                             |
|     `<class>.update(<ID>, <dictionary representation>)`    |                   Updates an objects based on a dictionary representation of attribute names and values                  |

## More Info
### Execution
Your shell should work like this in interactive mode:

```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
(hbnb) 
(hbnb) quit
$
But also in non-interactive mode: (like the Shell project in C)

$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
```

### Examples

```
(hbnb) all MyModel
** class doesn't exist **
(hbnb) show BaseModel
** instance id missing **
(hbnb) show BaseModel Holberton
** no instance found **
(hbnb) create BaseModel
49faff9a-6318-451f-87b6-910505c55907
(hbnb) all BaseModel
["[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'id': '49faff9a-6318-451f-87b6-910505c55907', 'updated_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903300)}"]
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'id': '49faff9a-6318-451f-87b6-910505c55907', 'updated_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903300)}
(hbnb) destroy
** class name missing **
(hbnb) update BaseModel 49faff9a-6318-451f-87b6-910505c55907 first_name "Betty"
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'first_name': 'Betty', 'id': '49faff9a-6318-451f-87b6-910505c55907', 'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'updated_at': datetime.datetime(2017, 10, 2, 3, 11, 3, 49401)}
(hbnb) create BaseModel
2dd6ef5c-467c-4f82-9521-a772ea7d84e9
(hbnb) all BaseModel
["[BaseModel] (2dd6ef5c-467c-4f82-9521-a772ea7d84e9) {'id': '2dd6ef5c-467c-4f82-9521-a772ea7d84e9', 'created_at': datetime.datetime(2017, 10, 2, 3, 11, 23, 639717), 'updated_at': datetime.datetime(2017, 10, 2, 3, 11, 23, 639724)}", "[BaseModel] (49faff9a-6318-451f-87b6-910505c55907) {'first_name': 'Betty', 'id': '49faff9a-6318-451f-87b6-910505c55907', 'created_at': datetime.datetime(2017, 10, 2, 3, 10, 25, 903293), 'updated_at': datetime.datetime(2017, 10, 2, 3, 11, 3, 49401)}"]
(hbnb) destroy BaseModel 49faff9a-6318-451f-87b6-910505c55907
(hbnb) show BaseModel 49faff9a-6318-451f-87b6-910505c55907
** no instance found **
(hbnb) 
```

```
(hbnb) User.count()
2
(hbnb) 
```

```
(hbnb) User.show("38f22813-2753-4d42-b37c-57a17f1e4f88")
[User] (38f22813-2753-4d42-b37c-57a17f1e4f88) {'age': 23, 'first_name': 'Bob', 'last_name': 'Holberton', 'created_at': datetime.datetime(2017, 9, 28, 21, 11, 42, 848279), 'updated_at': datetime.datetime(2017, 9, 28, 21, 15, 32, 299055), 'password': 'b9be11166d72e9e3ae7fd407165e4bd2', 'email': 'airbnb@holbertonshool.com', 'id': '38f22813-2753-4d42-b37c-57a17f1e4f88'}
(hbnb) 
(hbnb) User.update("38f22813-2753-4d42-b37c-57a17f1e4f88", {'first_name': "John", "age": 89})
(hbnb) 
(hbnb) User.show("38f22813-2753-4d42-b37c-57a17f1e4f88")
[User] (38f22813-2753-4d42-b37c-57a17f1e4f88) {'age': 89, 'first_name': 'John', 'last_name': 'Holberton', 'created_at': datetime.datetime(2017, 9, 28, 21, 11, 42, 848279), 'updated_at': datetime.datetime(2017, 9, 28, 21, 17, 10, 788143), 'password': 'b9be11166d72e9e3ae7fd407165e4bd2', 'email': 'airbnb@holbertonshool.com', 'id': '38f22813-2753-4d42-b37c-57a17f1e4f88'}
(hbnb) 
```

---

## Author
* **Farrukh Akhrarov** - [narnat](https://www.github.com/narnat)
* **Ethan Mayer** - [ethanpasta](https://www.github.com/ethanpasta)
