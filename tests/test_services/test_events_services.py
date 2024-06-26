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

# Test fetching a user by ID when the user exists
async def test_get_by_id_event_not_exists(db_session, event):
    non_existent_event_id = "non-existent--event-id"
    retrieved_event = await EventService.get_by_id(db_session, non_existent_event_id)
    assert retrieved_event is None

# Test updating a user with valid data
async def test_update_event_valid_data(db_session, event):
    title = "New Title"
    updated_user = await EventService.update(db_session, event.id, {"title": title})
    assert updated_user is not None
    assert updated_user.title == title

 # Test updating a user with valid data
async def test_update_event_invalid_data(db_session, event):
    updated_user = await EventService.update(db_session, event.id, {})
    assert updated_user is None

# Test updating a user with invalid data
async def test_update_event_invalid_eventid(db_session, event):
    non_existent_event_id = "non-existent--event-id"
    title = "New Title"
    updated_user = await EventService.update(db_session, non_existent_event_id, {"title": title})
    assert updated_user is None

# Test deleting a event with invalid eventid
async def test_delete_event_invalid_eventid(db_session):
    non_existent_event_id = "non-existent--event-id"
    updated_user = await EventService.delete(db_session, non_existent_event_id)
    assert updated_user is False

# Test deleting an event with valid data
async def test_delete_event_valid_data(db_session, event):
    updated_user = await EventService.delete(db_session, event.id)
    assert updated_user

# Test event counter
async def test_count_event_data(db_session):
    updated_user = await EventService.count(db_session)
    assert updated_user>=0

# Test all events
async def test_all_event_data(db_session):
    updated_user = await EventService.get_all_events(db_session,0,1)
    assert len(updated_user)>=0