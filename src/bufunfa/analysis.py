"""The math. Pure functions, no I/O.

The whole point of bufunfa: the LLM never does arithmetic. Compounding twelve monthly
rates in its head is exactly where a model gets a number subtly wrong, so the tools
return numbers computed here, together with the method used.

Contract: tests/test_analysis.py (start with the golden test: IPCA 2024 = 4.83%)
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

from bufunfa.models import Observation, Series


@dataclass(frozen=True)
class Change:
    value_pct: float
    method: str  # human-readable, goes back to the agent
    first_date: date
    last_date: date
    observations: int


def window(observations: Sequence[Observation], start: date, end: date) -> list[Observation]:
    # TODO: inclusive on both ends.
    raise NotImplementedError


def accumulated_change(rates_pct: Sequence[float]) -> float:
    """Compound period rates: [1, 1] -> 2.01 (not 2.0)."""
    # TODO: (product of (1 + r/100)) - 1, back to %. math.prod helps. Empty list -> 0.
    raise NotImplementedError


def level_change(first: float, last: float) -> float:
    # TODO: (last / first - 1) * 100; first == 0 -> ValueError.
    raise NotImplementedError


def change_over_period(series: Series, observations: Sequence[Observation]) -> Change:
    """Pick the method from series.kind (see models.Kind)."""
    # TODO: PERIOD_PCT -> accumulated_change; LEVEL -> level_change(first, last);
    #       ANNUAL_RATE -> ValueError explaining why ("... is an annual rate ...") and
    #       what to use instead (selic_diaria). The message goes straight to the agent.
    # TODO: no observations -> ValueError, never 0%.
    raise NotImplementedError


def real_change(nominal_pct: float, inflation_pct: float) -> float:
    """Growth above inflation: salary +10% with inflation +5% is +4.76% real, not +5%."""
    # TODO: divide, don't subtract.
    raise NotImplementedError


def adjust_for_inflation(value: float, inflation_pct: float) -> float:
    """What `value` at the start of the period is worth in end-of-period money."""
    raise NotImplementedError
