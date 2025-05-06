# FastAPI application routes for the Library System

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get list of all books
@app.get("/books")
def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

# Add a new book
@app.post("/books")
def create_book(title: str, author: str, db: Session = Depends(get_db)):
    return crud.add_book(db, title, author)

# Add a new member
@app.post("/members")
def create_member(name: str, email: str, db: Session = Depends(get_db)):
    return crud.add_member(db, name, email)

# Borrow a book
@app.post("/borrow")
def borrow_book(member_id: int, book_id: int, db: Session = Depends(get_db)):
    borrowing = crud.create_borrowing(db, member_id, book_id)
    if not borrowing:
        raise HTTPException(status_code=400, detail="Book unavailable or not found")
    return borrowing

# Return a borrowed book
@app.post("/return")
def return_borrow(borrow_id: int, db: Session = Depends(get_db)):
    result = crud.return_book(db, borrow_id)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid borrow ID or already returned")
    return result
