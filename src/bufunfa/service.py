"""Glue: catalog -> cache -> source API. The MCP tools only talk to this class.

No contract test of its own: tests/test_server.py replaces it with a fake, and the
roadmap has you run it once against the real APIs (step 6).
"""

from __future__ import annotations

from datetime import date

import httpx

from bufunfa.cache import Cache
from bufunfa.models import Observation, Series


def source_url(series: Series) -> str:
    """A link a human can open to check the number. Goes back to the agent for citation."""
    # TODO: BCB -> the SGS JSON URL for series.sgs_code; IBGE -> https://sidra.ibge.gov.br/tabela/<table>
    raise NotImplementedError


class Bufunfa:
    def __init__(self, client: httpx.Client | None = None, cache: Cache | None = None):
        # TODO: defaults from config.get_settings(): httpx.Client with User-Agent + timeout,
        #       Cache(settings.cache_path, settings.cache_ttl_seconds)
        raise NotImplementedError

    def observations(
        self, series_id: str, start: date, end: date
    ) -> tuple[Series, list[Observation]]:
        # TODO: catalog.get -> cache key "<id>:<start>:<end>" -> cache hit? return it
        # TODO: miss -> bcb.fetch(client, series.sgs_code, ...) or ibge.fetch(client, series, ...)
        #       -> cache.put -> return (series, observations)
        raise NotImplementedError
