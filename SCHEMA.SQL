This SQL script creates a database schema for a contact management system.
-- It includes three tables: 'contact_groups', 'contacts', and 'logs'.

-- Create a new database
CREATE DATABASE ContactDB;

-- Switch to the new database
USE ContactDB;

-- Create 'contact_groups' table (renaming 'groups' to avoid reserved keyword issues)
-- This table will store groups (like "Friends", "Family", etc.)
CREATE TABLE contact_groups (
    -- 'id' column is an auto-incrementing primary key
    id INT AUTO_INCREMENT PRIMARY KEY, 
    
    -- 'name' column to store the name of the group (e.g. "Friends", "Family")
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Create 'contacts' table to store contact information (name, email, phone, etc.)
CREATE TABLE contacts (
    -- 'id' column is an auto-incrementing primary key for each contact
    id INT AUTO_INCREMENT PRIMARY KEY, 
    
    -- 'name' column to store contact's name (first and last)
    name VARCHAR(100) NOT NULL, 
    
    -- 'email' column to store contact's email address (must be unique)
    email VARCHAR(100) UNIQUE,
    
    -- 'phone' column to store contact's phone number
    phone VARCHAR(15),
    
    -- 'group_id' is a foreign key, linking to the 'contact_groups' table
    group_id INT
);

-- Create 'logs' table to store actions related to contacts (like updates, deletions)
CREATE TABLE logs (
    -- 'id' column is an auto-incrementing primary key
    id INT AUTO_INCREMENT PRIMARY KEY, 
    
    -- 'contact_id' references the 'id' of the contact in the 'contacts' table
    contact_id INT NOT NULL, 
    
    -- 'action' column to describe what was done (e.g. "added", "updated", "deleted")
    action VARCHAR(50) NOT NULL,
    
    -- 'timestamp' column to store the date and time when the action occurred
    -- Default value is the current timestamp when the record is created
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
