# models/models.py
from pydantic import BaseModel
from typing import Optional

# Define the 'Member' model for request data validation
class Member(BaseModel):
    name: str            # Member's full name
    email: str           # Member's email address
    join_date: str       # Date the member joined (in 'YYYY-MM-DD' format)

# Define the 'MemberUpdate' model for updating member details
class MemberUpdate(BaseModel):
    name: Optional[str]  # Optional: Update name
    email: Optional[str] # Optional: Update email
    join_date: Optional[str] # Optional: Update join date
