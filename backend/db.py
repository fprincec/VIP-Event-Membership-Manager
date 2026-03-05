# From lines 3 to 18, I asked chatGPT how to write a Python function that establishes a connection to a MySQL database using the pymsql library.

import os # This line imports the os module
import pymysql # This line imports the pymysql library
from dotenv import load_dotenv # This line imports the load_dotenv function from the dotenv library

load_dotenv() # This line loads the environment variables from a .env file

def get_connection(): # This line defines a function named get_connection
    return pymysql.connect( # This line returns a connection object created by pymysql.conect() funtion
        host=os.getenv("DB_HOST"), 
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor, # This line sets the cursor class to DictCursor, which returns query results as dictionaries
        autocommit=True # This line enables autocommit, which means that each SQL statement is committed to the database immediately after its executed
    )