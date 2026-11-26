"""The curated list of series bufunfa knows about, and a search over it.

Why curate instead of exposing every SGS code? An agent can't guess that "salário mínimo"
is SGS 1619, or that IPCA food is IBGE table 7060, category 7170. The catalog is the
part of the server that turns a vague question into the right series.
"""

from __future__ import annotations

from bufunfa.models import Kind, Series, Source

SERIES: tuple[Series, ...] = (
    Series(
        id="ipca",
        name="IPCA — variação mensal",
        source=Source.BCB,
        kind=Kind.PERIOD_PCT,
        unit="%",
        frequency="monthly",
        sgs_code=433,
        description="Inflação oficial do Brasil, variação mensal.",
        aliases=("inflação", "inflation", "custo de vida", "preços"),
    ),
    Series(
        id="ipca_alimentos",
        name="IPCA — Alimentação e bebidas, variação mensal",
        source=Source.IBGE,
        kind=Kind.PERIOD_PCT,
        unit="%",
        frequency="monthly",
        ibge_table=7060,  # IPCA from Jan/2020 (POF 2017-2018 basket)
        ibge_variable=63,  # variação mensal
        ibge_classification="315[7170]",  # TODO(roadmap): confirm 7170 in /metadados
        description="Inflação de comida e bebida (grupo do IPCA). Disponível desde jan/2020.",
        aliases=("comida", "alimentos", "food", "mercado", "supermercado"),
    ),
    Series(
        id="ipca_ibge",
        name="IPCA — índice geral via IBGE, variação mensal",
        source=Source.IBGE,
        kind=Kind.PERIOD_PCT,
        unit="%",
        frequency="monthly",
        ibge_table=7060,
        ibge_variable=63,
        ibge_classification="315[7169]",
        description="O mesmo IPCA, direto do IBGE: serve pra conferir uma fonte com a outra.",
        aliases=("inflação ibge",),
    ),
    Series(
        id="salario_minimo",
        name="Salário mínimo",
        source=Source.BCB,
        kind=Kind.LEVEL,
        unit="R$",
        frequency="monthly",
        sgs_code=1619,
        description="Valor nominal do salário mínimo nacional vigente no mês.",
        aliases=("mínimo", "salario", "minimum wage", "piso"),
    ),
    Series(
        id="dolar",
        name="Dólar comercial — venda",
        source=Source.BCB,
        kind=Kind.LEVEL,
        unit="R$/US$",
        frequency="daily",
        sgs_code=1,
        description="Taxa de câmbio livre, dólar americano, venda, diária.",
        aliases=("câmbio", "cambio", "usd", "dollar"),
    ),
    Series(
        id="selic_meta",
        name="Meta Selic definida pelo Copom",
        source=Source.BCB,
        kind=Kind.ANNUAL_RATE,
        unit="% a.a.",
        frequency="daily",
        sgs_code=432,
        description="Taxa básica de juros (meta). É uma taxa ao ano: não se acumula.",
        aliases=("juros", "selic", "interest rate", "copom"),
    ),
    Series(
        id="selic_diaria",
        name="Taxa Selic diária",
        source=Source.BCB,
        kind=Kind.PERIOD_PCT,
        unit="% a.d.",
        frequency="daily",
        sgs_code=11,
        description="Selic efetiva ao dia. Acumulando, dá o rendimento da Selic num período.",
        aliases=("selic acumulada", "rendimento selic", "juros acumulados"),
    ),
)

_BY_ID = {s.id: s for s in SERIES}

_STOPWORDS = frozenset(
    "de da do das dos a o as os e em no na nos nas um uma por para pra com qual quanto "
    "the of in on and to for a an is what how much".split()
)


def _normalize(text: str) -> str:
    """'Inflação' -> 'inflacao': lowercase, no accents."""
    # TODO: unicodedata.normalize("NFKD", ...) then drop non-ASCII.
    raise NotImplementedError


def search(query: str, limit: int = 5) -> list[Series]:
    """Rank series by how many query words appear in id, name, aliases and description."""
    # TODO: normalize the query, split into words, drop _STOPWORDS
    #       (lesson learned: "de" matches every description in Portuguese).
    # TODO: score = how many times the words appear in a normalized "haystack" built from
    #       id (with "_" -> " "), name, aliases and description. Drop score 0.
    # TODO: sort by score desc, then id, and cut at `limit`.
    raise NotImplementedError


def get(series_id: str) -> Series:
    """Exact lookup. Unknown ids raise KeyError with suggestions, so the agent can recover."""
    # TODO: _BY_ID lookup; on miss, KeyError("unknown series 'x'; did you mean one of [...]?")
    #       using search(series_id) for the suggestions (all ids if search finds nothing).
    raise NotImplementedError
