from enum import Enum
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel


class EventType(str, Enum):
    view = "view"
    click = "click"
    purchase = "purchase"
    action = "action"


class EventIn(BaseModel):
    event_id: Optional[UUID] = None
    user_id: str
    item_id: str
    event_type: EventType
    metadata: Optional[Dict[str, Any]] = None


class EventOut(BaseModel):
    event_id: str
    status: str


class RecommendationItem(BaseModel):
    item_id: Optional[str]
    score: Optional[float]
    title: Optional[str] = None


class RecommendationsResponse(BaseModel):
    items: List[RecommendationItem]

#These are pydantic models and they define the shape of the HTTP request and response bodies
#Pydantic allows you to bypass __init__. Takes care of the __init__, validation, serialization, and error messages.
