from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.models import JobApplication, Status


def test_status_enum_has_six_values() -> None:
    from src.config import Settings

    assert len(Status) == 6
    assert Settings.model_fields["db_path"].default == "data/tracker.db"


def test_status_enum_values() -> None:
    assert Status.APPLIED.value == "applied"
    assert Status.INTERVIEW.value == "interview"
    assert Status.TEST_TASK.value == "test_task"
    assert Status.OFFER.value == "offer"
    assert Status.REJECTED.value == "rejected"
    assert Status.GHOSTED.value == "ghosted"


def test_job_application_valid_creation() -> None:
    created_at = datetime(2025, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
    updated_at = datetime(2025, 1, 1, tzinfo=timezone.utc)  # noqa: UP017

    app = JobApplication(
        id=1,
        user_id=123,
        company="Test Company",
        position="Python Developer",
        url="https://example.com/job",
        status=Status.INTERVIEW,
        created_at=created_at,
        updated_at=updated_at,
    )

    assert app.id == 1
    assert app.user_id == 123
    assert app.company == "Test Company"
    assert app.position == "Python Developer"
    assert app.url == "https://example.com/job"
    assert app.status == Status.INTERVIEW
    assert app.created_at == created_at
    assert app.updated_at == updated_at


def test_job_application_url_optional() -> None:
    app = JobApplication(
        id=2,
        user_id=123,
        company="No URL Inc",
        position="Backend Developer",
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),  # noqa: UP017
        updated_at=datetime(2025, 1, 1, tzinfo=timezone.utc),  # noqa: UP017
    )

    assert app.url is None


def test_job_application_default_status() -> None:
    app = JobApplication(
        id=3,
        user_id=123,
        company="Default Status LLC",
        position="Engineer",
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),  # noqa: UP017
        updated_at=datetime(2025, 1, 1, tzinfo=timezone.utc),  # noqa: UP017
    )

    assert app.status == Status.APPLIED


def test_job_application_invalid_status_rejected() -> None:
    with pytest.raises(ValidationError):
        JobApplication(
            id=4,
            user_id=123,
            company="Invalid Status Corp",
            position="QA",
            status="invalid",
            created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),  # noqa: UP017
            updated_at=datetime(2025, 1, 1, tzinfo=timezone.utc),  # noqa: UP017
        )
