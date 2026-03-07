#1. from lines 3 to 43 and 211 to 212, I asked chatGPT how to write a flask application that connects to a MySQL database, provides a health check endpoint, a database test endpoint, and an endpoint to initialize the database using a schema.sql file. 

from flask import Flask, jsonify #1. PT.1               START # This line imports the Flask class to create the application and jsonify to return JSON responses.
from flask_cors import CORS # This line imports CORS to enable Cross-Origin Resourse Sharing, allowing the frontend to commmunicate with the backend without CORS issues.
from db import get_connection # This line imports the get_connection funcion from the db module, which is responsible for esablishing a connection to the MySQL database.

app = Flask(__name__) # This line creates an instane of the Flask application and assigns it to the variable app.
CORS(app) # This line enables CORS for the Flask application to allow cross-origin requests from the frontend.

@app.get("/health") # This line defines a route for the health check endpoint using the GET method.
def health(): # This line defines the health function that will be called when the /health endpoint is accessed.
    return jsonify({"status": "server running"}) # This line returns a JSON response indicating that the server is running when the /health endpoint is accessed.

@app.get("/db-test") # This line defines a GET endpoint at the URL route /db-test.
def db_test(): # This line creates a function that will run when the /db-test endpoint is accessed
    try: # This line starts a try block to catch any database or connection errors
        conn = get_connection() # This line calls a function that creates and returns a connection to the database
        with conn.cursor() as cur: # This line opens a database cursor (used to execute SQL queries)
            cur.execute("SELECT 1 AS test") # This line runs a simple SQL query to test if the database connection works.
            result = cur.fetchone() # This line retrieves the first row returned from the query result.

        return jsonify({"database": "connected", "result": result}) # This line sends a JSON response confirming connection and returning query result.

    except Exception as e: # This line catches any error that occurs inside the try block
        return jsonify({"error": str(e)}), 500 # This line returns the error message as JSON with HTTP status code 500

@app.post("/init-db") # This line creates a POST endpoint at the route /init-db
def init_db(): # This is a function that runs when the /init-db endpoint is called
    try: # This line starts a try block to handle any errors that might occur
        conn = get_connection() # This line establishes a connection to the database using the get_connection() function

        with open("schema.sql") as f: # This line opens the schema.sql file which contains SQL commands to create database tables
            schema = f.read() # This line reads the entire contents of the schema.sql file into the variable 'schema'

        with conn.cursor() as cur: # This line creates a database cursor used to execute SQL commands
            for statement in schema.split(";"): # This line splits the SQL file into individual statements separated by semicolons
                if statement.strip(): # This line checks that the statement is not empty 
                    cur.execute(statement) # This line executes the SQL statement on the database

        return jsonify({"message": "Database initialized"}) # This line returns a JSON response indicating the database was successfully initialized

    except Exception as e: # This line catches any errors that occur during execution
        return jsonify({"error": str(e)}), 500 #1. PT.1             END This line returns the error message in JSON format with HTTP status code 500

#2. From lines 46 to 125, I asked chatGPT how to write Flask endpoints for CRUD operations on a "member" resource that will interact with a MySQL database using the get_connection function. 
from flask import request #2. START.           This line imports the request object from Flask so the server can access data sent by the client

@app.get("/members") # This line creates a GET endpoint at /members that will return all members
def get_members(): # This line defines the function that runs when the /members endpoint is accessed
    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
        cur.execute("SELECT * FROM member") # This line executes a SQL query to retrieve all records from the member table
        members = cur.fetchall() # This line retrieves all rows returned from the query and stores them in the variable members

    return jsonify(members) # This line converts the members data into JSON format and sends it back to the client

@app.get("/members/<int:member_id>") # This line creates a GET endpoint that retrieves a specific member using their ID
def get_member(member_id): # This line defines a function that accepts member_id from the URL parameter
    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object for executing SQL queries
        cur.execute("SELECT * FROM member WHERE id = %s", (member_id,)) # This line runs a SQL query to retrieve the member whose id matches the provided member_id
        member = cur.fetchone() # This line retrieves the first matching row from the query result

    if not member: # This line checks if no member was found with the given ID
        return jsonify({"error": "Member not found"}), 404 # This line returns a JSON error message with HTTP status code 404 if the member does not exist

    return jsonify(member) # This line converts the retrieved member data into JSON and returns it to the client

@app.post("/members") # This line creates a POST endpoint at /members used to add a new member to the database
def create_member(): # This line defines the function that runs when a POST request is sent to /members
    data = request.json # This line retrieves the JSON data sent in the request body and stores it in the variable data

    name = data.get("name") # This line extracts the value for "name" from the request data
    details = data.get("details") # This line extracts the value for "details" from the request data
    title = data.get("title") # This line extracts the value for "title" from the request data
    level = data.get("level") # This line extracts the value for "level" from the request data

    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a database cursor used to execute SQL queries
        cur.execute( # This line executes a SQL command to insert a new record into the member table
            """
            INSERT INTO member (name, details, title, level)
            VALUES (%s, %s, %s, %s)
            """, # This line defines the SQL statement that inserts values into the member table columns
            (name, details, title, level), # This line provides the values that will be inserted into the table
        )

        member_id = cur.lastrowid # This line retrieves the ID of the newly inserted member record

    return jsonify({"message": "Member created", "id": member_id}), 201 # This line returns a JSON response confirming creation and includes the new member's ID with HTTP status code 201

@app.put("/members/<int:member_id>") # This line creates a PUT endpoint used to update an existing member by their ID
def update_member(member_id): # This line defines the function that runs when a PUT request is sent to this endpoint and receives the member_id from the URL
    data = request.json # This line retrieves the JSON data sent in the request body and stores it in the variable data

    name = data.get("name") # This line extracts the "name" value from the request data
    details = data.get("details") # This line extracts the "details" value from the request data
    title = data.get("title") # This line extracts the "title" value from the request data
    level = data.get("level") # This line extracts the "level" value from the request data

    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
        cur.execute( # This line executes a SQL command to update an existing member record
            """
            UPDATE member
            SET name=%s, details=%s, title=%s, level=%s
            WHERE id=%s
            """, # This line defines the SQL update statement that modifies the member record
            (name, details, title, level, member_id), # This line supplies the values that will replace the existing values in the table
        )

    return jsonify({"message": "Member updated"}) # This line returns a JSON response confirming that the member was successfully updated

@app.delete("/members/<int:member_id>") # This line creates a DELETE endpoint used to remove a specific member using their ID
def delete_member(member_id): # This line defines the function that runs when a DELETE request is sent to this endpoint and receives the member_id from the URL
    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
        cur.execute("DELETE FROM member WHERE id=%s", (member_id,)) # This line executes a SQL query that deletes the member whose ID matches member_id

    return jsonify({"message": "Member deleted"}) #2.          END This line returns a JSON response confirming that the member was successfully deleted

# 3. From lines 128 to 209, I asked chatGPT how to write Flask endpoints for CRUD operations on an "event" resource that will interact with a MySQL database using the get_connection function.
@app.get("/events") # 3.       START This line creates a GET endpoint at /events used to retrieve all events from the database
def get_events(): # This line defines the function that runs when a request is made to the /events endpoint
    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
        cur.execute("SELECT * FROM event") # This line executes a SQL query that retrieves all records from the event table
        events = cur.fetchall() # This line retrieves all rows returned by the query and stores them in the variable events

    return jsonify(events) # This line converts the events data into JSON format and sends it back to the client

@app.get("/events/<int:event_id>") # This line creates a GET endpoint used to retrieve a specific event by its ID
def get_event(event_id): # This line defines the function that runs when the endpoint is accessed and receives event_id from the URL
    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
        cur.execute("SELECT * FROM event WHERE id = %s", (event_id,)) # This line executes a SQL query to retrieve the event whose id matches event_id
        event = cur.fetchone() # This line retrieves the first matching row returned from the query

    if not event: # This line checks whether the query returned no event
        return jsonify({"error": "Event not found"}), 404 # This line returns a JSON error message with HTTP status code 404 if the event does not exist

    return jsonify(event) # This line converts the event data into JSON format and returns it to the client

@app.post("/events") # This line creates a POST endpoint at /events used to create a new event in the database
def create_event(): # This line defines the function that runs when a POST request is sent to the /events endpoint
    data = request.json # This line retrieves the JSON data sent in the request body and stores it in the variable data

    name = data.get("name") # This line extracts the "name" value from the request data
    capacity = data.get("capacity") # This line extracts the "capacity" value from the request data
    level = data.get("level") # This line extracts the "level" value from the request data
    date = data.get("date") # This line extracts the "date" value from the request data

    conn = get_connection() # This line establishes a connection to the database

    try: # This line begins a try block to catch any errors that occur while inserting the event
        with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
            cur.execute( # This line executes a SQL command to insert a new event record into the event table
                """
                INSERT INTO event (name, capacity, level, date)
                VALUES (%s, %s, %s, %s)
                """, # This line defines the SQL insert statement for the event table
                (name, capacity, level, date), # This line supplies the values that will be inserted into the event table
            )

            event_id = cur.lastrowid # This line retrieves the ID of the newly inserted event record

        return jsonify({"message": "Event created", "id": event_id}), 201 # This line returns a JSON response confirming the event was created and includes the new event ID with HTTP status code 201

    except Exception as e: # This line catches any error that occurs inside the try block
        return jsonify({"error": str(e)}), 400 # This line returns the error message in JSON format with HTTP status code 400

@app.put("/events/<int:event_id>") # This line creates a PUT endpoint used to update an existing event using its ID
def update_event(event_id): # This line defines the function that runs when a PUT request is sent to this endpoint and receives event_id from the URL
    data = request.json # This line retrieves the JSON data sent in the request body and stores it in the variable data

    name = data.get("name") # This line extracts the "name" value from the request data
    capacity = data.get("capacity") # This line extracts the "capacity" value from the request data
    level = data.get("level") # This line extracts the "level" value from the request data
    date = data.get("date") # This line extracts the "date" value from the request data

    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
        cur.execute( # This line executes a SQL command to update an existing event record
            """
            UPDATE event
            SET name=%s, capacity=%s, level=%s, date=%s
            WHERE id=%s
            """, # This line defines the SQL update statement for modifying the event record
            (name, capacity, level, date, event_id), # This line supplies the values that will replace the existing values in the event table
        )

    return jsonify({"message": "Event updated"}) # This line returns a JSON response confirming that the event was successfully updated

@app.delete("/events/<int:event_id>") # This line creates a DELETE endpoint used to remove an event using its ID
def delete_event(event_id): # This line defines the function that runs when a DELETE request is sent to this endpoint and receives event_id from the URL
    conn = get_connection() # This line establishes a connection to the database

    with conn.cursor() as cur: # This line creates a cursor object used to execute SQL queries
        cur.execute("DELETE FROM event WHERE id=%s", (event_id,)) # This line executes a SQL query that deletes the event whose ID matches event_id

    return jsonify({"message": "Event deleted"}) # 3.           END This line returns a JSON response confirming that the event was successfully deleted

if __name__ == "__main__": #1. PT 2 START.        This line checks if the script is being run directly rather than imported as a module
    app.run(debug=True) # 1.   PT.2   END.     This line starts the Flask development server and enables debug mode for easier troubleshooting