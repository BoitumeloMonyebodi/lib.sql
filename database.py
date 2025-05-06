# db/database.py
import mysql.connector

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host="localhost",  # Your MySQL server host
        user="root",       # Your MySQL username
        password="",       # Your MySQL password
        database="LibraryDB"  # Database name
    )
