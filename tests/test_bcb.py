"""Contract for bufunfa.sources.bcb. No network: httpx.MockTransport plays the SGS API."""

import json
from datetime import date, timedelta
from pathlib import Path

import httpx
import pytest

from bufunfa.sources import bcb

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "sgs_433_ipca_2024.json").read_text())


def test_short_range_is_one_window():
    assert bcb.date_windows(date(2024, 1, 1), date(2024, 12, 31)) == [
        (date(2024, 1, 1), date(2024, 12, 31))
    ]


def test_long_range_is_split_into_contiguous_windows_of_at_most_10_years():
    start, end = date(2000, 1, 1), date(2025, 12, 31)
    windows = bcb.date_windows(start, end)

    assert len(windows) == 3
    assert windows[0][0] == start and windows[-1][1] == end
    for (_, prev_end), (next_start, _) in zip(windows, windows[1:], strict=False):
        assert next_start == prev_end + timedelta(days=1)  # no gaps, no overlaps
    for window_start, window_end in windows:
        assert window_end < window_start.replace(year=window_start.year + 10)


def test_start_after_end_is_an_error():
    with pytest.raises(ValueError):
        bcb.date_windows(date(2025, 1, 1), date(2024, 1, 1))


def test_build_params_uses_brazilian_dates():
    params = bcb.build_params(date(2024, 1, 5), date(2024, 12, 31))
    assert params == {"formato": "json", "dataInicial": "05/01/2024", "dataFinal": "31/12/2024"}


def test_parse():
    observations = bcb.parse(FIXTURE + [{"data": "01/01/2025", "valor": ""}])
    assert len(observations) == 12  # blank value skipped
    assert observations[0].date == date(2024, 1, 1)
    assert observations[0].value == pytest.approx(0.42)
    assert observations[7].value == pytest.approx(-0.02)


def test_fetch_splits_long_ranges_and_merges():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(dict(request.url.params))
        assert request.url.path == "/dados/serie/bcdata.sgs.433/dados"
        return httpx.Response(200, json=FIXTURE)  # same rows every time -> must dedupe

    client = httpx.Client(transport=httpx.MockTransport(handler))
    observations = bcb.fetch(client, 433, date(2000, 1, 1), date(2025, 12, 31))

    assert len(calls) == 3
    assert len(observations) == 12
    assert [o.date for o in observations] == sorted(o.date for o in observations)
