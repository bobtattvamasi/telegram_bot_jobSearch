from pathlib import Path

import pytest

from src.storage import Storage


@pytest.fixture
async def storage(tmp_path: Path) -> Storage:
    """Create a fresh Storage instance with a temporary database."""
    db_path = str(tmp_path / "test.db")
    s = Storage(db_path)
    await s.init_db()
    return s
