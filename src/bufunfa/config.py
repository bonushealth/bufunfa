"""Runtime settings from environment variables (see .env.example)."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    cache_path: Path
    cache_ttl_seconds: int
    timeout_s: float
    user_agent: str


def get_settings() -> Settings:
    default_cache = Path.home() / ".cache" / "bufunfa" / "cache.sqlite"
    return Settings(
        cache_path=Path(os.getenv("BUFUNFA_CACHE_PATH", default_cache)).expanduser(),
        cache_ttl_seconds=int(os.getenv("BUFUNFA_CACHE_TTL_SECONDS", str(12 * 60 * 60))),
        timeout_s=float(os.getenv("BUFUNFA_TIMEOUT_S", "30")),
        user_agent=os.getenv(
            "BUFUNFA_USER_AGENT", "bufunfa/0.1 (+https://github.com/bonushealth/bufunfa)"
        ),
    )
