# models/user.py
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
import uuid

class UserModel(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    service_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class UserSchemaRequest(SQLModel):
    service_name: str = Field(..., description="Name of the service")
    password: str = Field(..., description="Password")

class UserSchemaResponse(SQLModel):
    id: uuid.UUID
    service_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    service_name: Union[str, None] = None