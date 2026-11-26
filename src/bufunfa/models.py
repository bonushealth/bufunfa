"""Small, boring data types shared by every module."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum


class Source(StrEnum):
    BCB = "bcb"  # Banco Central, SGS
    IBGE = "ibge"  # IBGE, API de agregados (SIDRA)


class Kind(StrEnum):
    """How a series may be summarized over a period. This is what keeps the math honest.

    PERIOD_PCT   % change per period (IPCA monthly, Selic daily): compound to accumulate.
    LEVEL        a value in units (minimum wage R$, dollar R$/US$): compare first vs last.
    ANNUAL_RATE  a rate quoted per year (Selic target % a.a.): never accumulate, only show.
    """

    PERIOD_PCT = "period_pct"
    LEVEL = "level"
    ANNUAL_RATE = "annual_rate"


@dataclass(frozen=True)
class Observation:
    date: date
    value: float


@dataclass(frozen=True)
class Series:
    id: str
    name: str
    source: Source
    kind: Kind
    unit: str
    frequency: str  # "daily" | "monthly"
    description: str = ""
    aliases: tuple[str, ...] = ()
    sgs_code: int | None = None
    ibge_table: int | None = None
    ibge_variable: int | None = None
    ibge_classification: str | None = None  # e.g. "315[7170]"
    notes: tuple[str, ...] = field(default=())

    def to_dict(self) -> dict:
        """JSON-friendly dict for the agent: enums as strings, empty fields dropped."""
        # TODO: dataclasses.asdict(self); source/kind -> .value; drop None, () and "".
        raise NotImplementedError


def parse_period(text: str, *, end: bool = False) -> date:
    """'2020' / '2020-03' / '2020-03-15' -> date.

    With end=True a partial date means the *last* day: '2020' -> 2020-12-31,
    '2020-02' -> 2020-02-29. That's how "from 2020-01 to 2024-12" includes December.
    """
    # TODO: split on "-"; 1, 2 or 3 parts; calendar.monthrange(year, month)[1] gives the
    #       last day of a month (leap years included). Anything else -> ValueError.
    raise NotImplementedError
