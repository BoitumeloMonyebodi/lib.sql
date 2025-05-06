from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# MySQL connection string (change username, password as needed)
DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/ContactDB"

# Set up the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ========================
# Database Models
# ========================

# Group model (e.g., Friends, Family, Work)
class Group(Base):
    tablename = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    contacts = relationship("Contact", back_populates="group")

# Contact model
class Contact(Base):
    tablename = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(15))
    group_id = Column(Integer, ForeignKey("groups.id"))  # FK to groups table
    group = relationship("Group", back_populates="contacts")

# Log model for tracking actions on contacts
class Log(Base):
    tablename = "logs"
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"))
    action = Column(String(50), nullable=False)
    timestamp = Column(String(50), server_default="CURRENT_TIMESTAMP")

# Automatically create tables if not already present
Base.metadata.create_all(bind=engine)

# ========================
# Pydantic Schemas
# ========================

# Input schema for creating/updating a contact
class ContactCreate(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    group_id: Optional[int]

# Output schema for returning contact data
class ContactResponse(ContactCreate):
    id: int
    class Config:
        orm_mode = True

# ========================
# FastAPI App Initialization
# ========================

app = FastAPI()

# ========================
# CRUD Endpoints
# ========================

# Create a new contact
@app.post("/contacts/", response_model=ContactResponse)
def create_contact(contact: ContactCreate):
    db = SessionLocal()
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)

    # Log the creation
    db_log = Log(contact_id=db_contact.id, action="created")
    db.add(db_log)
    db.commit()

    db.close()
    return db_contact

# Get all contacts
@app.get("/contacts/", response_model=List[ContactResponse])
def get_contacts():
    db = SessionLocal()
    contacts = db.query(Contact).all()
    db.close()
    return contacts

# Get a single contact by ID
@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# Update an existing contact
@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact_data: ContactCreate):
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        db.close()
        raise HTTPException(status_code=404, detail="Contact not found")

    for key, value in contact_data.dict().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)

    # Log the update
    db_log = Log(contact_id=contact.id, action="updated")
    db.add(db_log)
    db.commit()

    db.close()
    return contact
# Delete a contact
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    db = SessionLocal()
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        db.close()
        raise HTTPException(status_code=404, detail="Contact not found")

    # Log before deletion
    db_log = Log(contact_id=contact.id, action="deleted")
    db.add(db_log)
    db.commit()

    db.delete(contact)
    db.commit()
    db.close()
    return {"message": "Contact deleted"}

# ========================
# Optional: Get Logs of Actions
# ========================

@app.get("/logs/")
def get_logs():
    db = SessionLocal()
    logs = db.query(Log).all()
    db.close()
    return logs