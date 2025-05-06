from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from typing import List, Optional

# ================================
# Function to get the MySQL database connection
# ================================
def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    """
    return mysql.connector.connect(
        host="localhost",  # Your MySQL server host
        user="root",       # Your MySQL username
        password="",       # Your MySQL password
        database="LibraryDB"  # Database name (from the schema in Question 1)
    )

# Initialize the FastAPI app
app = FastAPI()

# ================================
# Pydantic Models
# ================================
# Define the 'Member' model to validate incoming member data
class Member(BaseModel):
    name: str            # Member's full name
    email: str           # Member's email address
    join_date: str       # Date the member joined the library (in 'YYYY-MM-DD' format)

# Define 'MemberUpdate' model for updating member details
class MemberUpdate(BaseModel):
    name: Optional[str]  # Optional: Update name
    email: Optional[str] # Optional: Update email
    join_date: Optional[str] # Optional: Update join date

# ======================================================
# CRUD Operations for the Library Management System
# ======================================================

# CREATE: Add a new member to the database
@app.post("/members/", response_model=Member)
def create_member(member: Member):
    """
    Adds a new member to the 'Members' table in the MySQL database.
    Takes 'name', 'email', and 'join_date' as inputs.
    """
    connection = get_db_connection()  # Get DB connection
    cursor = connection.cursor(dictionary=True)  # Create a cursor for executing SQL queries
    
    # SQL query to insert a new member into the 'Members' table
    query = "INSERT INTO Members (name, email, join_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (member.name, member.email, member.join_date))  # Execute the query
    connection.commit()  # Commit the transaction to save changes
    cursor.close()  # Close the cursor
    connection.close()  # Close the database connection
    
    return member  # Return the created member as a response

# READ: Get all members from the database
@app.get("/members/", response_model=List[Member])
def get_members():
    """
    Retrieves all members from the 'Members' table.
    """
    connection = get_db_connection()  # Get DB connection
    cursor = connection.cursor(dictionary=True)  # Create a cursor for executing SQL queries
    
    query = "SELECT * FROM Members"  # SQL query to select all members
    cursor.execute(query)  # Execute the query
    members = cursor.fetchall()  # Fetch all the rows from the result of the query
    
    cursor.close()  # Close the cursor
    connection.close()  # Close the database connection
    
    return members  # Return the list of all members

# READ: Get a specific member by ID
@app.get("/members/{member_id}", response_model=Member)
def get_member(member_id: int):
    """
    Retrieves a specific member from the 'Members' table by member ID.
    """
    connection = get_db_connection()  # Get DB connection
    cursor = connection.cursor(dictionary=True)  # Create a cursor for executing SQL queries
    
    query = "SELECT * FROM Members WHERE member_id = %s"  # SQL query to select a member by ID
    cursor.execute(query, (member_id,))  # Execute the query with the member_id as a parameter
    member = cursor.fetchone()  # Fetch a single result (one member)
    
    cursor.close()  # Close the cursor
    connection.close()  # Close the database connection
    
    if member is None:
        # If no member is found, return a 404 error
        raise HTTPException(status_code=404, detail="Member not found")
    
    return member  # Return the found member

# UPDATE: Update a member's information
@app.put("/members/{member_id}", response_model=Member)
def update_member(member_id: int, member_update: MemberUpdate):
    """
    Updates a member's details (name, email, join_date) by member ID.
    """
    connection = get_db_connection()  # Get DB connection
    cursor = connection.cursor(dictionary=True)  # Create a cursor for executing SQL queries
    
    # Check if the member exists in the database
    cursor.execute("SELECT * FROM Members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()  # Fetch the member data
    
    if member is None:
        # If the member doesn't exist, return a 404 error
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Update fields if provided in the request (optional fields)
    if member_update.name:
        cursor.execute("UPDATE Members SET name = %s WHERE member_id = %s", (member_update.name, member_id))
    if member_update.email:
        cursor.execute("UPDATE Members SET email = %s WHERE member_id = %s", (member_update.email, member_id))
    if member_update.join_date:
        cursor.execute("UPDATE Members SET join_date = %s WHERE member_id = %s", (member_update.join_date, member_id))
    
    connection.commit()  # Commit the transaction
    cursor.close()  # Close the cursor
    connection.close()  # Close the database connection
    
    # Return the updated member data
    return {**member, **member_update.dict(exclude_unset=True)}

# DELETE: Delete a member by ID
@app.delete("/members/{member_id}")
def delete_member(member_id: int):
    """
    Deletes a member by their member ID.
    """
    connection = get_db_connection()  # Get DB connection
    cursor = connection.cursor()  # Create a cursor for executing SQL queries
    
    # Check if the member exists before deleting
    cursor.execute("SELECT * FROM Members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()  # Fetch the member data
    
    if member is None:
        # If the member doesn't exist, return a 404 error
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Member not found")
    
    # SQL query to delete the member from the database
    cursor.execute("DELETE FROM Members WHERE member_id = %s", (member_id,))
    connection.commit()  # Commit the transaction
    
    cursor.close()  # Close the cursor
    connection.close()  # Close the database connection
    
    return {"message": "Member deleted successfully"}  # Return a success message
