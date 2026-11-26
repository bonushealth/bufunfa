"""A tiny SQLite cache, so the same question doesn't hit BCB/IBGE twice in a row.

Contract: tests/test_cache.py
"""

from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

from bufunfa.models import Observation


class Cache:
    def __init__(self, path: Path, ttl_seconds: int, clock: Callable[[], float] = time.time):
        """`clock` is injectable so tests can travel in time instead of sleeping."""
        self.path = Path(path)
        self.ttl_seconds = ttl_seconds
        self.clock = clock
        # TODO: create the parent folder; sqlite3.connect(path) does not.
        # TODO: create table if not exists cache
        #       (key text primary key, payload text, stored_at real)
        raise NotImplementedError

    def get(self, key: str) -> list[Observation] | None:
        # TODO: None if missing OR older than ttl_seconds (compare with self.clock()).
        # TODO: payload is JSON [[iso_date, value], ...] -> Observations.
        raise NotImplementedError

    def put(self, key: str, observations: list[Observation]) -> None:
        # TODO: "insert or replace" with stored_at = self.clock(). Always use ? placeholders.
        raise NotImplementedError
