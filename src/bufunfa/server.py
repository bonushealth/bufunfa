"""The MCP server: five tools an agent can call.

Run it: `bufunfa` (stdio). Add to Claude Code:
    claude mcp add --transport stdio bufunfa -- bufunfa

Contract: tests/test_server.py (goes through a real MCP client, in memory)
"""

# No `from __future__ import annotations`: the SDK reads these type hints at runtime
# to build each tool's input schema.

from collections.abc import Iterator
from contextlib import contextmanager

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from bufunfa import catalog
from bufunfa.service import Bufunfa

INSTRUCTIONS = """\
Brazilian economic data from Banco Central (SGS) and IBGE.
1. Call search_series to find the series_id. Never guess ids.
2. For any accumulated change, comparison or inflation adjustment, call the tool:
   do not compute or estimate numbers yourself.
3. Report the method and cite the source_url that each tool returns.
4. If a series does not exist here, say so instead of answering from memory.
Dates: 'YYYY', 'YYYY-MM' or 'YYYY-MM-DD'. A partial end date includes the whole month/year.
"""

mcp = MCPServer("bufunfa", instructions=INSTRUCTIONS)

_service: Bufunfa | None = None


def service() -> Bufunfa:
    """Created on first use, so importing this module never opens sockets or files."""
    global _service
    if _service is None:
        _service = Bufunfa()
    return _service


@contextmanager
def agent_errors() -> Iterator[None]:
    """Turn expected errors into ToolError, so the agent sees the message and can recover.

    In mcp 2.x any other exception reaches the agent as an opaque "Error executing tool",
    and the agent can't tell "wrong id, try ipca" from "the server is broken".
    """
    try:
        yield
    except (KeyError, ValueError) as error:
        raise ToolError(error.args[0] if error.args else str(error)) from error


def _change(series_id: str, start: str, end: str) -> dict:
    """Shared by three tools: fetch the period and compute its change."""
    # TODO: service().observations(series_id, parse_period(start), parse_period(end, end=True))
    # TODO: analysis.change_over_period(series, observations)
    # TODO: return {"series_id", "name", "change_pct" (round 4), "method", "first_date",
    #       "last_date", "observations", "source_url"}
    raise NotImplementedError


# --- Worked example: the one tool that is done. Copy its shape for the others. ---------


@mcp.tool()
def search_series(query: str) -> dict:
    """Find Brazilian economic series by keyword, in Portuguese or English.

    Start here: returns series ids, units and what each series means.
    """
    with agent_errors():
        return {"results": [series.to_dict() for series in catalog.search(query)]}


# --- Your turn. The docstrings are what the agent reads: keep them precise. ----------


@mcp.tool()
def get_series(series_id: str, start: str, end: str, max_points: int = 500) -> dict:
    """Raw observations of one series between start and end (inclusive)."""
    # TODO: {"series": series.to_dict(), "observations": [{"date", "value"}...][:max_points],
    #        "truncated": bool, "source_url": ...}
    #  Daily series over 10 years = ~2500 points: truncate, and say so.
    raise NotImplementedError


@mcp.tool()
def change_over_period(series_id: str, start: str, end: str) -> dict:
    """Total % change of a series over a period, computed the right way for its kind.

    Monthly/daily rates are compounded; levels (R$, R$/US$) compare last vs first;
    annual rates (Selic target) are refused, because accumulating them is meaningless.
    """
    # TODO: with agent_errors(): return _change(...)
    raise NotImplementedError


@mcp.tool()
def compare_change(series_a: str, series_b: str, start: str, end: str) -> dict:
    """Compare two series over the same period, e.g. minimum wage vs food inflation.

    real_change_pct is how much A grew above B, as in "salary grew X% above prices".
    """
    # TODO: {"a": _change(a), "b": _change(b), "difference_pp": a - b,
    #        "real_change_pct": analysis.real_change(a, b)}
    raise NotImplementedError


@mcp.tool()
def adjust_for_inflation(value: float, start: str, end: str, index: str = "ipca") -> dict:
    """What an amount of money at `start` is worth in `end` money, using an inflation index."""
    # TODO: {"value", "adjusted_value" (round 2), "inflation": _change(index, start, end)}
    raise NotImplementedError


def main() -> None:
    mcp.run()  # stdio


if __name__ == "__main__":
    main()
