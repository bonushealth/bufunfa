"""Banco Central SGS API.

Rules that shape this module:
  * dates go in and come out as dd/MM/yyyy;
  * values come as strings with a dot decimal ("0.42");
  * since 26/03/2025, a query may span at most 10 years, so long ranges are split.

Contract: tests/test_bcb.py
"""

from __future__ import annotations

from datetime import date

import httpx

from bufunfa.models import Observation

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
MAX_YEARS = 10


def date_windows(start: date, end: date, max_years: int = MAX_YEARS) -> list[tuple[date, date]]:
    """Split [start, end] into consecutive windows no longer than `max_years`."""
    # TODO: start > end -> ValueError.
    # TODO: walk a cursor from start: window_end = min(cursor + 10 years - 1 day, end),
    #       next cursor = window_end + 1 day. No gaps, no overlaps.
    # Pegadinha: date(2016, 2, 29).replace(year=2026) explodes (no Feb 29 in 2026).
    raise NotImplementedError


def build_params(start: date, end: date) -> dict[str, str]:
    # TODO: {"formato": "json", "dataInicial": "dd/mm/yyyy", "dataFinal": "dd/mm/yyyy"}
    raise NotImplementedError


def parse(payload: list[dict]) -> list[Observation]:
    # TODO: each row is {"data": "01/01/2024", "valor": "0.42"}; skip empty "valor".
    raise NotImplementedError


def fetch(client: httpx.Client, code: int, start: date, end: date) -> list[Observation]:
    """Download [start, end], one request per 10-year window, merged and sorted by date."""
    # TODO: for each window: client.get(BASE_URL.format(code=code), params=build_params(...))
    # TODO: find out what SGS answers for a window with no data (empty list? 404?) and handle it.
    # TODO: merge into a dict keyed by date (windows may repeat rows), return sorted.
    raise NotImplementedError
