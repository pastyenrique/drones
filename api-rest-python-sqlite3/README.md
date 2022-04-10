# REST API using Flask, Python, SQLite3 and JSON
API created with Python using the Flask framework and the SQLite3 database.
The API can be consumed with any programming language that supports HTTP requests or using Postman: 

# Code Explanation
For Drone Dispatch Controller, we have a database to manage the structure of models Drone and Medication, we have this database structure and the connection with sqlite on db.py archive. This archive will be imported from controllers.py and main.py.
Before we expose the database in the API, we are going to create a drone controller that will take care of all the operations to save, update, delete and get the drone and medication data. 
All these functions are inside a file called controller.py. Here we see several functions, the insert_drone function receives the drone data and inserts it into the database (INSERT); all this using prepared statements to avoid SQL injections in this API that we are creating with Python and Flask.
We also see other methods like load_medication, wich register a new medication in the database associated to a drone_id, update_drone which performs the UPDATE operation to update a drone, delete_drone which deletes a drone (DELETE) from its id and get_by_id which returns a drone from its id (using the SELECT operation).
Now that we have the CRUD of the operations with the database, it is time to expose everything in the API with Flask. The file that manage the API is main.py.
The first thing we do in the API is create the Flask app and import the drone controller. We also import a function from the database because we need to create the tables when starting the application:
Later we define all the functions that will be interacting with the API, these functions are:
-get_all_drones()
-insert_drone()
-load_medications_on_drone(drone_id)
-update_drone_state(drone_id)
-update_drone(id)
-delete_drone(id)
-get_drone_by_id(id)
-get_drone_by_state(state)
-get_medications_by_drone(id_drone)
-get_battery_level_by_drone(id_drone)
-get_all_drones_battery_level()

In all these functions we define the routes with the methods GET, PUT, POST and DELETE. Each route exposes a drone controller function we saw earlier, which in turn interacts with the SQLite3 database. 
It is important to highlight a few things. For example, when updating, inserting a drone and load medication on a drone, we read the JSON from the request with get_json and access the dictionary. In the case of delete or get by ID we read the id variable from the route as <id> and receive it in the method.
This Python API communicates via JSON, so many responses are made according to what the jsonify function returns.

In the case of get_all_drones_battery_level function, it is called from an external archive, wich will be executed as a scheduled task (in my case a Linux OS scheduled task), and will write on a log file called cron_log_batteries, a register of the battery percent of the drones on db.

Finally we create the Flask app to start the server and listen for requests:

# Execute Project and testing the API
This is a Python Project on Flask Framework, so you have to install python and Flask, this application has been developed on Visual Studio Code ide, I will asume you will have python install on your computer, so here some comands on how to install a virtual environment, activate it, and at last, install Flask and run the application:
1-Command to install a virtual env: virtualenv -p python3 env
2-Activate the virtual env: .\env\Scripts\activate (or press Ctrl+Shift+P and select this virtualenv as your Python Interpreter)
3-Install Flask Command: pip install flask
4-Command to Run the project: python3 main.py (Run main.py archive to run the project)

Once the application is running, through the Postman application we can make requests to our server.
The JSON structure is next:

-To register a new drone:

{
    "serial_number": "asdew",
    "model": "Heavyweight",
    "weight_limit": 3.0,
    "battery_capacity": 45,
    "state": "IDLE"
}

-To load a medication:

{
    "medications": [
        {     
            "name": "Advil",   
            "weight": 2.0,
            "code": "SD456_",
            "image": "/home/pastor/Escritorio/Proyecto Musala/api-rest-python-sqlite3/medication_img"
        },
        {     
            "name": "Tylenol",
            "weight": 1.5,
            "code": "__POL",
            "image": "/home/pastor/Escritorio/Proyecto Musala/api-rest-python-sqlite3/medication_img"
        }
    ]
}

# Demo
To watch some demonstration images we can go to demo folder and watch some demonstration images.