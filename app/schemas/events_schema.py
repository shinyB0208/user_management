from builtins import bool, str
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional,List
from datetime import datetime
from enum import Enum
import uuid
from app.models.models import EventCategory

class EventBase(BaseModel):
    title : str = Field(..., example="Tech Conference 2023")
    category: EventCategory = Field(..., example=EventCategory.TECH)
    end_date: datetime = Field(..., example="2023-06-03T18:00:00")
    start_date: datetime = Field(..., example="2023-06-01T09:00:00")
    description: str = Field(..., example="Annual technology conference featuring keynotes and workshops.")
    location: str = Field(..., example="New York City, USA")

    @validator('start_date', 'end_date')
    def validate_dates(cls, value):
        if (value).astimezone(tz=None) < (datetime.now().astimezone(tz=None)):
            raise ValueError("Date must be in the future")
        return value

    @validator('end_date')
    def validate_end_date(cls, value, values):
        start_date = values.get('start_date')
        if start_date and (value).astimezone(tz=None) < (start_date.astimezone(tz=None)):
            raise ValueError("End date must be after start date")
        return value
    
    class Config:
        from_attributes = True

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    title: Optional[str] = Field(None, example="Updated Tech Conference 2023")
    description: Optional[str] = Field(None, example="Updated description for the tech conference.")
    start_date: Optional[datetime] = Field(None, example="2023-06-02T09:00:00")
    end_date: Optional[datetime] = Field(None, example="2023-06-04T18:00:00")
    location: Optional[str] = Field(None, example="San Francisco, USA")
    category: Optional[EventCategory] = Field(None, example=EventCategory.TECH)

    @root_validator(pre=True)
    def check_at_least_one_value(cls, values):
        if not any(values.values()):
            raise ValueError("At least one field must be provided for update")
        return values

class EventResponse(EventBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    created_by : uuid.UUID = Field(..., example=uuid.uuid4()),
    title: Optional[str] = Field(None, example="Updated Tech Conference 2023")
    description: Optional[str] = Field(None, example="Updated description for the tech conference.")
    start_date: Optional[datetime] = Field(None, example="2023-06-02T09:00:00")
    end_date: Optional[datetime] = Field(None, example="2023-06-04T18:00:00")
    location: Optional[str] = Field(None, example="San Francisco, USA")
    category: Optional[EventCategory] = Field(None, example=EventCategory.TECH)


class EventListResponse(BaseModel):
    items: List[EventResponse] = Field(...)
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)