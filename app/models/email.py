from datetime import datetime, timezone
from typing import List, Optional
import uuid
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from enum import Enum

class EmailStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class EmailModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_email: EmailStr
    to_email: str
    to_cc_email: Optional[str] = None
    to_cco_email: Optional[str] = None
    subject: str
    attachment: Optional[str] = None
    body: str
    status: EmailStatus
    created_at: datetime = Field(default_factory=datetime.now)
    sent_at: Optional[datetime] = None
    # Foreign key to the user that owns the email
    owner_id: uuid.UUID = Field(foreign_key="usermodel.id")

class EmailSchemaRequest(SQLModel):
    from_email: EmailStr = Field(..., description="Email address of the sender")
    to_email: List[EmailStr] = Field(..., description="Email address of the recipient")
    to_cc_email: Optional[List[EmailStr]] = Field(None, description="Email address to be included in the CC field")
    to_cco_email: Optional[List[EmailStr]] = Field(None, description="Email address to be included in the BCC field")
    subject: str = Field(..., description="Subject of the email", min_length=1, max_length=50)
    body: str = Field(..., description="HTML content of the email", min_length=3)

class EmailSchemaResponse(SQLModel):
    id: int
    from_email: EmailStr
    to_email: str
    to_cc_email: Optional[str] = None
    to_cco_email: Optional[str] = None
    subject: str
    attachment: Optional[str] = None
    body: str
    status: EmailStatus
    created_at: datetime
    sent_at: Optional[datetime] = None
