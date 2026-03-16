import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database_session import new_async_session
from app.events.models import Event
from app.events.schemas import (
    EventCreate,
    EventListResponse,
    EventResponse,
    EventUpdate,
)
from app.guests.models import Guest

logger = logging.getLogger(__name__)

router = APIRouter()


def _event_to_response(event: Event, guest_count: int = 0) -> EventResponse:
    return EventResponse(
        event_id=event.event_id,
        title=event.title,
        description=event.description,
        event_date=event.event_date,
        event_time=event.event_time,
        location=event.location,
        occasion=event.occasion,
        status=event.status,
        guest_limit=event.guest_limit,
        is_rsvp_enabled=event.is_rsvp_enabled,
        host_id=event.host_id,
        guest_count=guest_count,
    )


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new event",
)
async def create_event(
    data: EventCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> EventResponse:
    event = Event(
        title=data.title,
        description=data.description,
        event_date=data.event_date,
        event_time=data.event_time,
        location=data.location,
        occasion=data.occasion,
        guest_limit=data.guest_limit,
        is_rsvp_enabled=data.is_rsvp_enabled,
        host_id=current_user.user_id,
    )
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return _event_to_response(event)


@router.get(
    "",
    response_model=EventListResponse,
    description="List current user's events",
)
async def list_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> EventListResponse:
    base_query = select(Event).where(
        Event.host_id == current_user.user_id,
        Event.is_deleted == False,  # noqa: E712
    )

    # Count total
    count_query = select(func.count()).select_from(base_query.subquery())
    total = await session.scalar(count_query) or 0

    # Paginate
    offset = (page - 1) * page_size
    events_query = base_query.offset(offset).limit(page_size).order_by(
        Event.event_date.desc()
    )
    result = await session.execute(events_query)
    events = result.scalars().all()

    # Get guest counts
    event_ids = [e.event_id for e in events]
    guest_counts: dict[str, int] = {}
    if event_ids:
        gc_query = (
            select(Guest.event_id, func.count(Guest.guest_id))
            .where(Guest.event_id.in_(event_ids))
            .group_by(Guest.event_id)
        )
        gc_result = await session.execute(gc_query)
        guest_counts = dict(gc_result.all())

    return EventListResponse(
        events=[
            _event_to_response(e, guest_counts.get(e.event_id, 0)) for e in events
        ],
        total=total,
    )


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    description="Get event details",
)
async def get_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> EventResponse:
    event = await session.get(Event, event_id)
    if event is None or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.host_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    gc_query = select(func.count(Guest.guest_id)).where(
        Guest.event_id == event.event_id
    )
    guest_count = await session.scalar(gc_query) or 0

    return _event_to_response(event, guest_count)


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    description="Update an event",
)
async def update_event(
    event_id: str,
    data: EventUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> EventResponse:
    event = await session.get(Event, event_id)
    if event is None or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.host_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(event, key):
            setattr(event, key, value.value if hasattr(value, "value") else value)

    session.add(event)
    await session.commit()
    await session.refresh(event)
    return _event_to_response(event)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Soft delete an event",
)
async def delete_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> None:
    event = await session.get(Event, event_id)
    if event is None or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.host_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    event.is_deleted = True
    session.add(event)
    await session.commit()
