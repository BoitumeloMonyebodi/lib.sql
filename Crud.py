# crud/crud.py
from typing import List, Optional
import mysql.connector
from models.models import Member, MemberUpdate
from fastapi import HTTPException
from db.database import get_db_connection

# ======================================================
# CRUD Operations
# ======================================================

# CREATE: Add a new member to the database
def create_member(member: Member):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "INSERT INTO Members (name, email, join_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (member.name, member.email, member.join_date))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return member

# READ: Get all members from the database
def get_members() -> List[Member]:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM Members"
    cursor.execute(query)
    members = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return members

# READ: Get a specific member by ID
def get_member_by_id(member_id: int) -> Optional[Member]:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM Members WHERE member_id = %s"
    cursor.execute(query, (member_id,))
    member = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return member

# UPDATE: Update member's information by ID
def update_member(member_id: int, member_update: MemberUpdate):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Check if the member exists
    cursor.execute("SELECT * FROM Members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()
    
    if member is None:
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
    
    connection.commit()
    cursor.close()
    connection.close()

    return {**member, **member_update.dict(exclude_unset=True)}

# DELETE: Delete a member by ID
def delete_member(member_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the member exists
    cursor.execute("SELECT * FROM Members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()

    if member is None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="Member not found")

    cursor.execute("DELETE FROM Members WHERE member_id = %s", (member_id,))
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return {"message": "Member deleted successfully"}
