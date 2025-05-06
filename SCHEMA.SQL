-- ============================
-- Create Database
-- ============================
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- ================================
-- Table: Authors
-- Stores details about authors, including their name and birth year.
-- ================================
CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique author ID, auto-incremented
    name VARCHAR(100) NOT NULL,                -- Author's name, cannot be NULL
    birth_year INT                             -- Year of birth of the author
);

-- ================================
-- Table: Publishers
-- Stores details about publishers.
-- ================================
CREATE TABLE Publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique publisher ID, auto-incremented
    name VARCHAR(100) NOT NULL UNIQUE            -- Publisher's name, must be unique
);

-- ================================
-- Table: Categories
-- Stores information about book categories (genres).
-- ================================
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique category ID, auto-incremented
    name VARCHAR(50) NOT NULL UNIQUE             -- Category name (e.g., Fantasy), must be unique
);

-- ================================
-- Table: Books
-- Stores details about books, including title, ISBN, author, publisher, and category.
-- ================================
CREATE TABLE Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique book ID, auto-incremented
    title VARCHAR(150) NOT NULL,                 -- Book title, cannot be NULL
    isbn VARCHAR(13) NOT NULL UNIQUE,            -- International Standard Book Number (ISBN), must be unique
    publisher_id INT,                            -- Foreign key to Publishers table
    category_id INT,                             -- Foreign key to Categories table
    author_id INT,                               -- Foreign key to Authors table
    year_published INT,                          -- Year the book was published
    -- Foreign key constraints:
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id), -- Links to Publishers table
    FOREIGN KEY (category_id) REFERENCES Categories(category_id), -- Links to Categories table
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)          -- Links to Authors table
);

-- ================================
-- Table: Members
-- Stores details about library members.
-- ================================
CREATE TABLE Members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique member ID, auto-incremented
    name VARCHAR(100) NOT NULL,                  -- Member's full name, cannot be NULL
    email VARCHAR(100) NOT NULL UNIQUE,          -- Member's email address, must be unique
    join_date DATE NOT NULL                      -- Date when the member joined the library
);

-- ================================
-- Table: Staff
-- Stores details about library staff members.
-- ================================
CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,     -- Unique staff ID, auto-incremented
    name VARCHAR(100) NOT NULL,                  -- Staff member's name, cannot be NULL
    position VARCHAR(50),                        -- Job title of the staff member
    hire_date DATE                               -- Date when the staff member was hired
);

-- ================================
-- Table: Borrow_Records
-- Tracks when books are borrowed and returned by members, including which staff processed the transaction.
-- ================================
CREATE TABLE Borrow_Records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique transaction record ID, auto-incremented
    member_id INT,                               -- Foreign key to Members table (the member who borrowed the book)
    book_id INT,                                 -- Foreign key to Books table (the book being borrowed)
    borrow_date DATE NOT NULL,                   -- Date when the book was borrowed, cannot be NULL
    return_date DATE,                            -- Date when the book was returned (nullable, can be NULL if not returned)
    staff_id INT,                                -- Foreign key to Staff table (staff who processed the transaction)
    -- Foreign key constraints:
    FOREIGN KEY (member_id) REFERENCES Members(member_id), -- Links to Members table
    FOREIGN KEY (book_id) REFERENCES Books(book_id),       -- Links to Books table
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)      -- Links to Staff table
);
