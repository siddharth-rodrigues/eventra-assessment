from datetime import date, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.events.models import EventStatus


class EventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: date
    event_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=500)
    occasion: Optional[str] = Field(None, max_length=100)
    guest_limit: Optional[int] = Field(None, ge=1)
    is_rsvp_enabled: bool = True


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: Optional[date] = None
    event_time: Optional[time] = None
    location: Optional[str] = Field(None, max_length=500)
    occasion: Optional[str] = Field(None, max_length=100)
    status: Optional[EventStatus] = None
    guest_limit: Optional[int] = Field(None, ge=1)
    is_rsvp_enabled: Optional[bool] = None


class EventResponse(BaseModel):
    event_id: str
    title: str
    description: Optional[str]
    event_date: date
    event_time: Optional[time]
    location: Optional[str]
    occasion: Optional[str]
    status: str
    guest_limit: Optional[int]
    is_rsvp_enabled: bool
    host_id: str
    guest_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class EventListResponse(BaseModel):
    events: list[EventResponse]
    total: int
