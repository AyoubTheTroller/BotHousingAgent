from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    authorized: bool
    created_at: datetime
    last_active: datetime
    language: str
