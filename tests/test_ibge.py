"""Contract for bufunfa.sources.ibge.

The fixture has the real response *shape* but SYNTHETIC values, plus the "-" and "..."
placeholders IBGE uses for missing data.
"""

import json
from datetime import date
from pathlib import Path

import httpx
import pytest

from bufunfa import catalog
from bufunfa.sources import ibge

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "ibge_7060_synthetic.json").read_text())


def test_build_url():
    url = ibge.build_url(7060, 63, date(2020, 1, 1), date(2025, 12, 31))
    assert url == (
        "https://servicodados.ibge.gov.br/api/v3/agregados/7060/periodos/202001-202512/variaveis/63"
    )


def test_build_params():
    assert ibge.build_params("315[7170]") == {
        "localidades": "N1[all]",
        "classificacao": "315[7170]",
    }
    assert ibge.build_params(None) == {"localidades": "N1[all]"}


def test_parse_skips_placeholders_instead_of_making_zeros():
    observations = ibge.parse(FIXTURE)
    assert [o.date for o in observations] == [
        date(2024, 1, 1),
        date(2024, 2, 1),
        date(2024, 4, 1),
        date(2024, 6, 1),
    ]
    assert observations[-1].value == pytest.approx(2.0)


def test_parse_refuses_ambiguous_payloads():
    two_categories = json.loads(json.dumps(FIXTURE))
    two_categories[0]["resultados"].append(two_categories[0]["resultados"][0])
    with pytest.raises(ValueError):
        ibge.parse(two_categories)


def test_fetch_sends_the_series_parameters():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["path"] = request.url.path
        seen["params"] = dict(request.url.params)
        return httpx.Response(200, json=FIXTURE)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    series = catalog.get("ipca_alimentos")
    observations = ibge.fetch(client, series, date(2024, 1, 1), date(2024, 6, 30))

    assert seen["path"] == "/api/v3/agregados/7060/periodos/202401-202406/variaveis/63"
    assert seen["params"] == {"localidades": "N1[all]", "classificacao": "315[7170]"}
    assert len(observations) == 4
