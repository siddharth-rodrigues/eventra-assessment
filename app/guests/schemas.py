from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class GuestCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)


class GuestResponse(BaseModel):
    guest_id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    is_attending: Optional[bool]
    rsvp_responded_at: Optional[datetime]
    event_id: str

    model_config = ConfigDict(from_attributes=True)


class GuestListResponse(BaseModel):
    guests: list[GuestResponse]
    total: int


class RSVPRequest(BaseModel):
    is_attending: bool
