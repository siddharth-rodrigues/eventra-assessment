import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.core.database_session import new_async_session
from app.events.models import Event
from app.guests.models import Guest
from app.guests.schemas import (
    GuestCreate,
    GuestListResponse,
    GuestResponse,
    RSVPRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter()


async def _get_event_for_owner(
    event_id: str, user: User, session: AsyncSession
) -> Event:
    event = await session.get(Event, event_id)
    if event is None or event.is_deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.host_id != user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return event


@router.post(
    "/events/{event_id}/guests",
    response_model=GuestResponse,
    status_code=status.HTTP_201_CREATED,
    description="Add a guest to an event",
)
async def add_guest(
    event_id: str,
    data: GuestCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> GuestResponse:
    event = await _get_event_for_owner(event_id, current_user, session)

    # Check guest limit
    if event.guest_limit is not None:
        count_query = select(func.count(Guest.guest_id)).where(
            Guest.event_id == event_id
        )
        current_count = await session.scalar(count_query) or 0
        if current_count >= event.guest_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Guest limit reached for this event",
            )

    guest = Guest(
        name=data.name,
        email=data.email,
        phone=data.phone,
        event_id=event_id,
    )
    session.add(guest)
    await session.commit()
    await session.refresh(guest)

    return GuestResponse(
        guest_id=guest.guest_id,
        name=guest.name,
        email=guest.email,
        phone=guest.phone,
        is_attending=guest.is_attending,
        rsvp_responded_at=guest.rsvp_responded_at,
        event_id=guest.event_id,
    )


@router.get(
    "/events/{event_id}/guests",
    response_model=GuestListResponse,
    description="List guests for an event",
)
async def list_guests(
    event_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(new_async_session),
) -> GuestListResponse:
    await _get_event_for_owner(event_id, current_user, session)

    base_query = select(Guest).where(Guest.event_id == event_id)
    count_query = select(func.count()).select_from(base_query.subquery())
    total = await session.scalar(count_query) or 0

    offset = (page - 1) * page_size
    guests_query = base_query.offset(offset).limit(page_size).order_by(
        Guest.created_at.desc()
    )
    result = await session.execute(guests_query)
    guests = result.scalars().all()

    return GuestListResponse(
        guests=[
            GuestResponse(
                guest_id=g.guest_id,
                name=g.name,
                email=g.email,
                phone=g.phone,
                is_attending=g.is_attending,
                rsvp_responded_at=g.rsvp_responded_at,
                event_id=g.event_id,
            )
            for g in guests
        ],
        total=total,
    )


@router.patch(
    "/{guest_id}/rsvp",
    response_model=GuestResponse,
    description="RSVP for a guest (public - no auth required)",
)
async def rsvp_guest(
    guest_id: str,
    data: RSVPRequest,
    session: AsyncSession = Depends(new_async_session),
) -> GuestResponse:
    guest = await session.get(Guest, guest_id)
    if guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")

    # Check if RSVP is enabled for the event
    event = await session.get(Event, guest.event_id)
    if event is None or not event.is_rsvp_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="RSVP is not enabled for this event",
        )

    guest.is_attending = data.is_attending
    guest.rsvp_responded_at = datetime.now(timezone.utc)
    session.add(guest)
    await session.commit()
    await session.refresh(guest)

    return GuestResponse(
        guest_id=guest.guest_id,
        name=guest.name,
        email=guest.email,
        phone=guest.phone,
        is_attending=guest.is_attending,
        rsvp_responded_at=guest.rsvp_responded_at,
        event_id=guest.event_id,
    )
