import json
from datetime import date
from pathlib import Path

import pytest

from bufunfa import analysis, catalog
from bufunfa.models import Observation
from bufunfa.sources import bcb

FIXTURE = Path(__file__).parent / "fixtures" / "sgs_433_ipca_2024.json"


@pytest.fixture
def ipca_2024():
    return bcb.parse(json.loads(FIXTURE.read_text()))


def test_golden_ipca_2024_matches_the_official_4_83(ipca_2024):
    """The 12 official monthly IPCA rates of 2024, compounded, give IBGE's 4.83% for the year.

    Source: IBGE, "IPCA em dezembro vai a 0,52% e acumula 4,83% em 2024" (10/01/2025).
    """
    change = analysis.change_over_period(catalog.get("ipca"), ipca_2024)
    assert round(change.value_pct, 2) == 4.83
    assert change.observations == 12
    assert change.first_date == date(2024, 1, 1)
    assert change.last_date == date(2024, 12, 1)


def test_accumulated_change_compounds_instead_of_adding():
    assert analysis.accumulated_change([1.0] * 12) == pytest.approx(12.6825, abs=1e-4)
    assert analysis.accumulated_change([]) == 0


def test_level_change():
    assert analysis.level_change(1412, 1518) == pytest.approx(7.5071, abs=1e-4)
    with pytest.raises(ValueError):
        analysis.level_change(0, 10)


def test_level_series_compares_last_vs_first():
    observations = [
        Observation(date(2024, 1, 1), 1412.0),
        Observation(date(2024, 6, 1), 1412.0),
        Observation(date(2025, 1, 1), 1518.0),
    ]
    change = analysis.change_over_period(catalog.get("salario_minimo"), observations)
    assert change.value_pct == pytest.approx(7.5071, abs=1e-4)
    assert "first" in change.method


def test_annual_rates_are_refused():
    observations = [Observation(date(2024, 1, 1), 11.75), Observation(date(2024, 12, 1), 12.25)]
    with pytest.raises(ValueError, match="annual rate"):
        analysis.change_over_period(catalog.get("selic_meta"), observations)


def test_empty_period_is_an_error_not_zero():
    with pytest.raises(ValueError):
        analysis.change_over_period(catalog.get("ipca"), [])


def test_window_is_inclusive(ipca_2024):
    picked = analysis.window(ipca_2024, date(2024, 3, 1), date(2024, 5, 1))
    assert [o.date.month for o in picked] == [3, 4, 5]


def test_real_change_divides_instead_of_subtracting():
    assert analysis.real_change(10, 5) == pytest.approx(4.7619, abs=1e-4)


def test_adjust_for_inflation():
    assert analysis.adjust_for_inflation(100, 4.83) == pytest.approx(104.83)
