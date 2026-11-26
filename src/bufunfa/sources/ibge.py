"""IBGE aggregates API (the JSON face of SIDRA), v3.

URL: /api/v3/agregados/{table}/periodos/{YYYYMM-YYYYMM}/variaveis/{variable}
     ?localidades=N1[all]&classificacao=315[7170]
Values come as strings keyed by period ("202401": "0.42"). Missing values use
placeholders like "-", "..." or "X" and must be skipped, not turned into zero.

Contract: tests/test_ibge.py
"""

from __future__ import annotations

from datetime import date

import httpx

from bufunfa.models import Observation, Series

BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"


def build_url(table: int, variable: int, start: date, end: date) -> str:
    # TODO: f"{BASE_URL}/{table}/periodos/{start:%Y%m}-{end:%Y%m}/variaveis/{variable}"
    raise NotImplementedError


def build_params(classification: str | None, locality: str = "N1[all]") -> dict[str, str]:
    # TODO: always "localidades"; "classificacao" only when given. N1[all] = Brasil.
    raise NotImplementedError


def parse(payload: list[dict]) -> list[Observation]:
    """Expect exactly one variable, one category, one locality. Anything else is a bug upstream."""
    # TODO: payload[0]["resultados"][0]["series"][0]["serie"] is {"202401": "0.42", ...}
    # TODO: more than one variable / result / series -> ValueError (narrow the query instead
    #       of silently picking one)
    # TODO: "-", "...", "X" -> skip. Never 0: a missing month is not a month without inflation.
    # TODO: period "YYYYMM" -> date(year, month, 1); return sorted by date.
    raise NotImplementedError


def fetch(client: httpx.Client, series: Series, start: date, end: date) -> list[Observation]:
    # TODO: build_url + build_params(series.ibge_classification) -> GET -> parse
    raise NotImplementedError
