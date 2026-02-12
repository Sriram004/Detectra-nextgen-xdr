from datetime import datetime
from pydantic import BaseModel, Field


class Alert(BaseModel):
    id: str
    rule_id: str
    severity: str
    status: str = "new"
    host_id: str
    user_id: str | None = None
    title: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence: float = 0.5


class Incident(BaseModel):
    id: str
    title: str
    severity: str
    priority: int
    status: str = "new"
    alert_ids: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PlaybookRunRequest(BaseModel):
    alert_id: str


class User(BaseModel):
    username: str
    role: str
