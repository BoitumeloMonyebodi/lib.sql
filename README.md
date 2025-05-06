# Library Management System

## Project Description
This is a **Library Management System** built with **FastAPI** and **MySQL**. It allows users to manage books, authors, publishers, categories, staff, and borrowing records. The system provides APIs for CRUD operations (Create, Read, Update, Delete) for books, members, and borrow records.

## Technologies Used
- **FastAPI**: Python web framework for building APIs.
- **MySQL**: Database for storing library data.
- **SQLAlchemy**: ORM for interacting with MySQL.
- **Pymysql**: MySQL database adapter for Python.

## Database Schema
The system has the following tables:
- **Authors**: Stores author information.
- **Publishers**: Stores publisher details.
- **Categories**: Stores book genres.
- **Books**: Stores book details and links to authors, publishers, and categories.
- **Members**: Stores library member information.
- **Staff**: Stores library staff information.
- **Borrow_Records**: Tracks borrowed books by members.

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
# Library Management API

This is a simple CRUD API for a Library Management System, built using **FastAPI** and **MySQL**.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd library-api

