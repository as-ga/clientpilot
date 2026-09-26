from datetime import datetime

from pydantic import BaseModel


class Client(BaseModel):
    id: str
    name: str
    external_id: str | None = None
    health: str = "unknown"
    created_at: datetime | None = None
