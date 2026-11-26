from datetime import date

from bufunfa.cache import Cache
from bufunfa.models import Observation

OBS = [Observation(date(2024, 1, 1), 0.42), Observation(date(2024, 2, 1), 0.83)]


class FakeClock:
    def __init__(self):
        self.now = 1_000.0

    def __call__(self) -> float:
        return self.now


def test_roundtrip(tmp_path):
    cache = Cache(tmp_path / "sub" / "cache.sqlite", ttl_seconds=60)
    cache.put("ipca:2024", OBS)
    assert cache.get("ipca:2024") == OBS
    assert cache.get("other") is None


def test_entries_expire(tmp_path):
    clock = FakeClock()
    cache = Cache(tmp_path / "cache.sqlite", ttl_seconds=60, clock=clock)
    cache.put("k", OBS)
    clock.now += 59
    assert cache.get("k") == OBS
    clock.now += 2
    assert cache.get("k") is None


def test_put_overwrites_and_survives_reopening(tmp_path):
    path = tmp_path / "cache.sqlite"
    Cache(path, ttl_seconds=60).put("k", OBS)
    Cache(path, ttl_seconds=60).put("k", OBS[:1])
    assert Cache(path, ttl_seconds=60).get("k") == OBS[:1]
