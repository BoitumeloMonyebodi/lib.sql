-- Create Database
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- ============================
-- Table: Authors
-- Stores book author details
-- ============================
CREATE TABLE Authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique author ID
    name VARCHAR(100) NOT NULL,                -- Author's name
    birth_year INT                             -- Year of birth
);

-- ============================
-- Table: Publishers
-- Stores book publisher details
-- ============================
CREATE TABLE Publishers (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY, -- Unique publisher ID
    name VARCHAR(100) NOT NULL UNIQUE            -- Publisher name (must be unique)
);

-- ============================
-- Table: Categories
-- Stores genres or categories for books
-- ============================
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique category ID
    name VARCHAR(50) NOT NULL UNIQUE             -- Category name (e.g., Fantasy)
);

-- ============================
-- Table: Books
-- Stores information about books
-- ============================
CREATE TABLE Books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,      -- Unique book ID
    title VARCHAR(150) NOT NULL,                 -- Book title
    isbn VARCHAR(13) NOT NULL UNIQUE,            -- International Standard Book Number
    publisher_id INT,                            -- FK to Publishers
    category_id INT,                             -- FK to Categories
    author_id INT,                               -- FK to Authors
    year_published INT,                          -- Year book was published
    FOREIGN KEY (publisher_id) REFERENCES Publishers(publisher_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
);

-- ============================
-- Table: Members
-- Library members who borrow books
-- ============================
CREATE TABLE Members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique member ID
    name VARCHAR(100) NOT NULL,                  -- Member's full name
    email VARCHAR(100) NOT NULL UNIQUE,          -- Member's email address
    join_date DATE NOT NULL                      -- Date the member joined the library
);

-- ============================
-- Table: Staff
-- Library staff who assist with lending
-- ============================
CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,     -- Unique staff ID
    name VARCHAR(100) NOT NULL,                  -- Staff member name
    position VARCHAR(50),                        -- Job title
    hire_date DATE                               -- Date of hiring
);

-- ============================
-- Table: Borrow_Records
-- Tracks when books are borrowed and returned
-- ============================
CREATE TABLE Borrow_Records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique transaction record ID
    member_id INT,                               -- FK to Members
    book_id INT,                                 -- FK to Books
    borrow_date DATE NOT NULL,                   -- Date of borrowing
    return_date DATE,                            -- Date of return (nullable)
    staff_id INT,                                -- FK to Staff who handled the transaction
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (staff_id) REFERENCES Staff(staff_id)
);

-- =======================================
-- Sample Data: Authors
-- =======================================
INSERT INTO Authors (name, birth_year) VALUES
('J.K. Rowling', 1965),
('George Orwell', 1903),
('J.R.R. Tolkien', 1892);

-- =======================================
-- Sample Data: Publishers
-- =======================================
INSERT INTO Publishers (name) VALUES
('Penguin Random House'),
('HarperCollins'),
('Bloomsbury');
-- =======================================
-- Sample Data: Categories
-- =======================================
INSERT INTO Categories (name) VALUES
('Fantasy'),
('Science Fiction'),
('Drama');

-- =======================================
-- Sample Data: Books
-- =======================================
INSERT INTO Books (title, isbn, publisher_id, category_id, author_id, year_published) VALUES
('Harry Potter and the Sorcerer''s Stone', '9780439554930', 3, 1, 1, 1997),
('1984', '9780451524935', 1, 2, 2, 1949),
('The Hobbit', '9780547928227', 2, 1, 3, 1937);

-- =======================================
-- Sample Data: Members
-- =======================================
INSERT INTO Members (name, email, join_date) VALUES
('Alice Smith', 'alice@example.com', '2023-01-15'),
('Bob Johnson', 'bob@example.com', '2022-09-10');

-- =======================================
-- Sample Data: Staff
-- =======================================
INSERT INTO Staff (name, position, hire_date) VALUES
('Emily White', 'Librarian', '2021-06-01'),
('Michael Green', 'Assistant', '2022-03-12');

-- =======================================
-- Sample Data: Borrow Records
-- =======================================
INSERT INTO Borrow_Records (member_id, book_id, borrow_date, return_date, staff_id) VALUES
(1, 1, '2023-11-10', '2023-11-20', 1),
(2, 2, '2023-12-01', NULL, 2);