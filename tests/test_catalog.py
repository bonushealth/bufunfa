import pytest

from bufunfa import catalog
from bufunfa.models import Source


@pytest.mark.parametrize(
    ("query", "expected_first"),
    [
        ("inflação", "ipca"),
        ("inflation", "ipca"),
        ("salário mínimo", "salario_minimo"),
        ("minimum wage", "salario_minimo"),
        ("comida", "ipca_alimentos"),
        ("dólar", "dolar"),
        ("selic acumulada", "selic_diaria"),
    ],
)
def test_search_finds_the_obvious_series_first(query, expected_first):
    results = catalog.search(query)
    assert results, f"nothing found for {query!r}"
    assert results[0].id == expected_first


def test_search_without_match_returns_empty():
    assert catalog.search("pib de jales") == []


def test_get_unknown_id_suggests_alternatives():
    with pytest.raises(KeyError, match="ipca"):
        catalog.get("ipca mensal")


def test_catalog_is_consistent():
    ids = [s.id for s in catalog.SERIES]
    assert len(ids) == len(set(ids))
    for series in catalog.SERIES:
        if series.source is Source.BCB:
            assert series.sgs_code, series.id
        else:
            assert series.ibge_table and series.ibge_variable, series.id
