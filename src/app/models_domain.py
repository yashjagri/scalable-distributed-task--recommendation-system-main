from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID


@dataclass
class User:
    id: Optional[UUID]
    email: str
    created_at: Optional[datetime] = None


@dataclass
class Item:
    id: Optional[UUID]
    metadata: Dict[str, Any]
    created_at: Optional[datetime] = None


@dataclass
class Event:
    id: Optional[UUID]
    user_id: UUID
    item_id: Optional[UUID]
    event_type: str
    value: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


@dataclass
class Recommendation:
    user_id: UUID
    item_id: UUID
    score: float
    updated_at: Optional[datetime] = None


#Postgres         →    ORM layer       →    Domain layer
#(rows and SQL)        (models_db.py)        (models_domain.py)
#                       knows SQL             knows nothing
# dataclass has __init__, __repr__, and __eq__ in itself already
#magic methods allow you to call methods without exlicitly stating them ex. a == b refers to __eq__
#you have all these layers so that if you were to switch to a different plaform, you could easily do so