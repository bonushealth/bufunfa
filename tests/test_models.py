from datetime import date

import pytest

from bufunfa.models import Kind, Series, Source, parse_period


@pytest.mark.parametrize(
    ("text", "end", "expected"),
    [
        ("2020", False, date(2020, 1, 1)),
        ("2020", True, date(2020, 12, 31)),
        ("2024-02", False, date(2024, 2, 1)),
        ("2024-02", True, date(2024, 2, 29)),  # leap year
        ("2023-02", True, date(2023, 2, 28)),
        ("2024-03-15", True, date(2024, 3, 15)),
    ],
)
def test_parse_period(text, end, expected):
    assert parse_period(text, end=end) == expected


def test_parse_period_rejects_garbage():
    with pytest.raises(ValueError):
        parse_period("2024-01-01-01")


def test_series_to_dict_is_json_friendly_and_skips_empty_fields():
    series = Series("x", "X", Source.BCB, Kind.LEVEL, "R$", "monthly", sgs_code=1)
    data = series.to_dict()
    assert data["source"] == "bcb"
    assert data["kind"] == "level"
    assert "ibge_table" not in data
    assert "aliases" not in data
