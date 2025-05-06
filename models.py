# SQLAlchemy models representing the tables in the Library Management System

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    available = Column(Integer, default=1)  # 1 = Available, 0 = Borrowed

    borrowings = relationship("Borrowing", back_populates="book")

class Member(Base):
    __tablename__ = 'members'

    member_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    borrowings = relationship("Borrowing", back_populates="member")

class Borrowing(Base):
    __tablename__ = 'borrowings'

    borrow_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('members.member_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    borrow_date = Column(Date)        # Date book was borrowed
    return_date = Column(Date)        # Date book was returned

    member = relationship("Member", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")
