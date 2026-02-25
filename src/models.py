"""Domain models for job applications and statuses."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):  # noqa: UP042
    """Application status values used in storage and handlers."""

    APPLIED = "applied"
    INTERVIEW = "interview"
    TEST_TASK = "test_task"
    OFFER = "offer"
    REJECTED = "rejected"
    GHOSTED = "ghosted"


class JobApplication(BaseModel):
    """Represents a single user job application record."""

    id: int
    user_id: int
    company: str
    position: str
    url: str | None = None
    status: Status = Status.APPLIED
    created_at: datetime
    updated_at: datetime
