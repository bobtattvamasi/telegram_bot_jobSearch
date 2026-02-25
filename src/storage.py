"""Async storage layer for job application CRUD operations."""

from datetime import UTC, datetime, timedelta

import aiosqlite

from src.models import JobApplication, Status


class ApplicationNotFound(Exception):  # noqa: N818
    """Raised when application does not exist or belongs to another user."""


class InvalidStatus(Exception):  # noqa: N818
    """Raised when an invalid status value is provided."""


class Storage:
    """Async SQLite storage for job applications."""

    def __init__(self, db_path: str) -> None:
        """Initialize storage with a database path.

        Args:
            db_path: Path to the SQLite database file.
        """
        self._db_path = db_path

    async def init_db(self) -> None:
        """Initialize database schema and indexes."""
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    company TEXT NOT NULL,
                    position TEXT NOT NULL,
                    url TEXT,
                    status TEXT NOT NULL DEFAULT 'applied',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            await db.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON applications(user_id);")
            await db.commit()

    async def add_application(
        self,
        user_id: int,
        company: str,
        position: str,
        url: str | None = None,
    ) -> JobApplication:
        """Insert a new application and return created model.

        Args:
            user_id: Telegram user identifier.
            company: Company name.
            position: Position title.
            url: Optional vacancy URL.

        Returns:
            Created job application model.
        """
        now = datetime.now(UTC)
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO applications (
                    user_id, company, position, url, status, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    company,
                    position,
                    url,
                    Status.APPLIED.value,
                    now.isoformat(),
                    now.isoformat(),
                ),
            )
            await db.commit()

            app_id = cursor.lastrowid
            if app_id is None:
                raise RuntimeError("Failed to insert application row")

        return JobApplication(
            id=app_id,
            user_id=user_id,
            company=company,
            position=position,
            url=url,
            status=Status.APPLIED,
            created_at=now,
            updated_at=now,
        )

    async def get_applications(
        self,
        user_id: int,
        status_filter: Status | None = None,
    ) -> list[JobApplication]:
        """Return applications for a user, optionally filtered by status.

        Args:
            user_id: Telegram user identifier.
            status_filter: Optional status filter.

        Returns:
            List of matching applications sorted by creation date desc.
        """
        query = "SELECT * FROM applications WHERE user_id = ?"
        params: list[object] = [user_id]

        if status_filter is not None:
            query += " AND status = ?"
            params.append(status_filter.value)

        query += " ORDER BY created_at DESC"

        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, tuple(params))
            rows = await cursor.fetchall()

        return [self._row_to_application(row) for row in rows]

    async def update_status(self, user_id: int, app_id: int, new_status: Status) -> JobApplication:
        """Update application status and return updated model.

        Args:
            user_id: Telegram user identifier.
            app_id: Application identifier.
            new_status: New application status.

        Raises:
            InvalidStatus: If provided status is invalid.
            ApplicationNotFound: If application is missing or belongs to another user.

        Returns:
            Updated application model.
        """
        try:
            status = new_status if isinstance(new_status, Status) else Status(str(new_status))
        except ValueError as error:
            raise InvalidStatus(str(new_status)) from error

        now = datetime.now(UTC)

        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                UPDATE applications
                SET status = ?, updated_at = ?
                WHERE id = ? AND user_id = ?
                """,
                (status.value, now.isoformat(), app_id, user_id),
            )

            if cursor.rowcount == 0:
                await db.rollback()
                raise ApplicationNotFound(f"Application #{app_id} was not found")

            await db.commit()

            selected = await db.execute(
                "SELECT * FROM applications WHERE id = ? AND user_id = ?",
                (app_id, user_id),
            )
            row = await selected.fetchone()

        if row is None:
            raise ApplicationNotFound(f"Application #{app_id} was not found")

        return self._row_to_application(row)

    async def delete_application(self, user_id: int, app_id: int) -> bool:
        """Delete an application owned by a user.

        Args:
            user_id: Telegram user identifier.
            app_id: Application identifier.

        Raises:
            ApplicationNotFound: If application is missing or belongs to another user.

        Returns:
            True when deletion succeeds.
        """
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(
                "DELETE FROM applications WHERE id = ? AND user_id = ?",
                (app_id, user_id),
            )

            if cursor.rowcount == 0:
                await db.rollback()
                raise ApplicationNotFound(f"Application #{app_id} was not found")

            await db.commit()

        return True

    async def get_stale_applications(self, user_id: int, days: int) -> list[JobApplication]:
        """Return applied applications not updated for more than given days.

        Args:
            user_id: Telegram user identifier.
            days: Stale threshold in days.

        Returns:
            List of stale applications.
        """
        cutoff = datetime.now(UTC) - timedelta(days=days)

        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                """
                SELECT * FROM applications
                WHERE user_id = ?
                  AND status = ?
                  AND updated_at < ?
                ORDER BY updated_at ASC
                """,
                (user_id, Status.APPLIED.value, cutoff.isoformat()),
            )
            rows = await cursor.fetchall()

        return [self._row_to_application(row) for row in rows]

    async def get_all_user_ids(self) -> list[int]:
        """Get all distinct user IDs from the database."""
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute("SELECT DISTINCT user_id FROM applications")
            rows = await cursor.fetchall()
            return [int(row[0]) for row in rows]

    async def get_stats(self, user_id: int) -> dict[str, int]:
        """Return status counters for a user with total count.

        Args:
            user_id: Telegram user identifier.

        Returns:
            Mapping of status to count and total key.
        """
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(
                """
                SELECT status, COUNT(*)
                FROM applications
                WHERE user_id = ?
                GROUP BY status
                """,
                (user_id,),
            )
            rows = await cursor.fetchall()

        stats = {str(status): int(count) for status, count in rows}
        stats["total"] = sum(stats.values())
        return stats

    def _row_to_application(self, row: aiosqlite.Row) -> JobApplication:
        """Convert a database row to JobApplication model.

        Args:
            row: SQLite row with application fields.

        Returns:
            Parsed application model.
        """
        created_at = self._parse_datetime(row["created_at"])
        updated_at = self._parse_datetime(row["updated_at"])

        return JobApplication(
            id=int(row["id"]),
            user_id=int(row["user_id"]),
            company=str(row["company"]),
            position=str(row["position"]),
            url=str(row["url"]) if row["url"] is not None else None,
            status=Status(str(row["status"])),
            created_at=created_at,
            updated_at=updated_at,
        )

    def _parse_datetime(self, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            parsed = value
        elif isinstance(value, str):
            normalized = value.replace("Z", "+00:00")
            parsed = datetime.fromisoformat(normalized)
        else:
            raise TypeError(f"Unsupported datetime type: {type(value)!r}")

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
