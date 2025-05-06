# CRUD operations for managing books, members, and borrowings

from sqlalchemy.orm import Session
import models
from datetime import date

# Retrieve all books
def get_books(db: Session):
    return db.query(models.Book).all()

# Add a new book
def add_book(db: Session, title: str, author: str):
    book = models.Book(title=title, author=author)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# Add a new library member
def add_member(db: Session, name: str, email: str):
    member = models.Member(name=name, email=email)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

# Create a borrowing record if book is available
def create_borrowing(db: Session, member_id: int, book_id: int):
    book = db.query(models.Book).filter(models.Book.book_id == book_id, models.Book.available == 1).first()
    if not book:
        return None  # Book not available
    book.available = 0  # Mark book as borrowed
    borrowing = models.Borrowing(member_id=member_id, book_id=book_id, borrow_date=date.today())
    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)
    return borrowing

# Return a borrowed book
def return_book(db: Session, borrow_id: int):
    borrowing = db.query(models.Borrowing).filter(models.Borrowing.borrow_id == borrow_id).first()
    if borrowing and not borrowing.return_date:
        borrowing.return_date = date.today()
        borrowing.book.available = 1  # Mark book as available
        db.commit()
        db.refresh(borrowing)
        return borrowing
    return None
