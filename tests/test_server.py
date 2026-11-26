"""The MCP server, exercised through a real MCP client (in memory, no network)."""

import asyncio
import json
from pathlib import Path

import pytest
from mcp import Client

from bufunfa import catalog, server
from bufunfa.sources import bcb

FIXTURE = Path(__file__).parent / "fixtures" / "sgs_433_ipca_2024.json"


class FakeService:
    """Stands in for Bufunfa: serves the IPCA 2024 fixture for every series."""

    def observations(self, series_id, start, end):
        ipca_2024 = bcb.parse(json.loads(FIXTURE.read_text()))
        return catalog.get(series_id), [o for o in ipca_2024 if start <= o.date <= end]


@pytest.fixture
def fake_service(monkeypatch):
    monkeypatch.setattr(server, "_service", FakeService())


def call(tool: str, **arguments):
    async def run():
        async with Client(server.mcp) as client:
            return await client.call_tool(tool, arguments)

    result = asyncio.run(run())
    text = result.content[0].text if result.content else ""
    return result.is_error, text


def test_tools_are_registered():
    """Green from day one: guards the wiring, not the logic."""

    async def run():
        async with Client(server.mcp) as client:
            return {tool.name for tool in (await client.list_tools()).tools}

    assert asyncio.run(run()) == {
        "search_series",
        "get_series",
        "change_over_period",
        "compare_change",
        "adjust_for_inflation",
    }


def test_search_series():
    is_error, text = call("search_series", query="inflação")
    assert not is_error
    assert json.loads(text)["results"][0]["id"] == "ipca"


def test_change_over_period(fake_service):
    is_error, text = call("change_over_period", series_id="ipca", start="2024", end="2024")
    assert not is_error, text
    body = json.loads(text)
    assert round(body["change_pct"], 2) == 4.83
    assert body["source_url"].startswith("https://api.bcb.gov.br/")


def test_errors_reach_the_agent_with_a_useful_message(fake_service):
    is_error, text = call("change_over_period", series_id="ipca mensal", start="2024", end="2024")
    assert is_error
    assert "did you mean" in text


def test_annual_rates_are_refused_with_an_explanation(fake_service):
    is_error, text = call("change_over_period", series_id="selic_meta", start="2024", end="2024")
    assert is_error
    assert "annual rate" in text
