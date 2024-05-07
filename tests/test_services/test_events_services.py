from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.models import Event, EventCategory
from app.services.events_service import EventService

pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_event_with_valid_data(db_session, admin_user):
    event_data = {
        "title": "Tech Conference",
        "category": EventCategory.TECH,
        "end_date": "2026-06-03T18:00:00",
        "start_date": "2026-06-01T09:00:00",
        "description": "Annual technology conference featuring keynotes and workshops.",
        "location": "New York City, USA"
    }
    event = await EventService.create(db_session, event_data, admin_user.id)
    assert event is not None
    assert event.title == event_data["title"]

async def test_create_event_with_invalid_data(db_session, admin_user):
    event_data = {
        "title": "Tech Conference",
    }
    event = await EventService.create(db_session, event_data, admin_user.id)
    assert event is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_event_exists(db_session, event):
    print(event)
    retrieved_event = await EventService.get_by_id(db_session, event.id)
    print(retrieved_event)
    assert retrieved_event.id == event.id