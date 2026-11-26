<p align="center">
  <img src="docs/assets/bufunfa-icon.svg" alt="bufunfa" width="112">
</p>

<h1 align="center">bufunfa</h1>

<p align="center">
  <b>Brazilian economic data for AI agents, with the math done right.</b><br>
  An MCP server over Banco Central (SGS) and IBGE: inflation, minimum wage, interest rates, exchange rates.
</p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-work%20in%20progress-2d8a5f">
  <img alt="python" src="https://img.shields.io/badge/python-3.11%2B-1d3557">
  <img alt="mcp" src="https://img.shields.io/badge/protocol-MCP-1d3557">
  <img alt="evals" src="https://img.shields.io/badge/evals-included-1d3557">
</p>

---

## Why

Ask a chatbot *"did the minimum wage keep up with food prices since 2020?"* and one of two things
happens: it answers from memory, or it finds some monthly numbers and compounds them in its head.
Both fail quietly, with a confident, plausible and wrong number.

**bufunfa** (Brazilian slang for money) gives any MCP-capable agent the official series and does
the arithmetic itself: compounding monthly rates, real growth, inflation adjustment. Every number
comes back with the method used and a link to the source, so the agent can cite it and a human can
check it.

It's for students, journalists, analysts, and anyone who wants their AI to stop guessing about
the Brazilian economy.

## What it looks like

```
You:    How much was Brazil's official inflation (IPCA) in 2024?

Agent → search_series("inflação")                        -> ipca (SGS 433, monthly %)
Agent → change_over_period("ipca", "2024", "2024")
        <- {"change_pct": 4.8313, "method": "compounded 12 monthly rates",
            "first_date": "2024-01-01", "last_date": "2024-12-01",
            "source_url": "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"}

Agent:  4.83% (12 monthly IPCA rates compounded; source: Banco Central SGS 433).
```

IBGE's official figure for 2024 is 4.83%, and the test suite checks that bufunfa gets the same.

## Tools

| Tool                    | What it does                                                                 |
| ----------------------- | ---------------------------------------------------------------------------- |
| `search_series`         | Find a series by keyword, in Portuguese or English. Always the first call.  |
| `get_series`            | Raw observations between two dates (truncated, and flagged, when too long). |
| `change_over_period`    | Total % change, computed the right way for the kind of series.              |
| `compare_change`        | Two series over the same period, plus real growth of A over B.              |
| `adjust_for_inflation`  | What an amount of money from then is worth in today's money.                |

## Series

| id                | Source        | Code                       | Kind        |
| ----------------- | ------------- | -------------------------- | ----------- |
| `ipca`            | Banco Central | SGS 433                    | monthly %   |
| `ipca_alimentos`  | IBGE          | table 7060, var 63, c315   | monthly %   |
| `ipca_ibge`       | IBGE          | table 7060, var 63, c315   | monthly %   |
| `salario_minimo`  | Banco Central | SGS 1619                   | level (R$)  |
| `dolar`           | Banco Central | SGS 1                      | level (R$/US$) |
| `selic_meta`      | Banco Central | SGS 432                    | annual rate |
| `selic_diaria`    | Banco Central | SGS 11                     | daily %     |

## Design decisions

1. **The model never does arithmetic.** Compounding twelve monthly rates is exactly where an LLM
   drifts by a few tenths. Tools return computed numbers, never "here's the data, you do the math".
2. **Series know what they are.** Monthly rates are compounded, levels compare last against first,
   and annual rates (the Selic target) are *refused* with an explanation, because "accumulated
   Selic target" is not a number that means anything.
3. **A curated catalog beats raw codes.** No agent can guess that the minimum wage is SGS 1619 or
   that food inflation is IBGE table 7060, category 7170. `search_series` turns words into ids.
4. **Errors are written for the agent.** An unknown id comes back as *"unknown series 'ipca mensal';
   did you mean ['ipca', ...]?"*, so the agent can correct itself instead of giving up.
5. **Every number carries its method and source.** The answer can be cited, and checked.
6. **Respect the upstream APIs.** SGS limits queries to 10 years, so long ranges are split and
   merged. A SQLite cache keeps repeated questions from hitting the APIs again.

## Evals

Unit tests prove the math. Evals check whether a real agent, given these tools, actually answers
correctly. Each case in [`cases.toml`](src/bufunfa/evals/cases.toml) uses one of three kinds of truth:

- **`expected`**: a figure published by the official source, checked by hand, with a link;
- **`expected_from`**: computed by bufunfa from the raw data, through the same tool, trustworthy
  because the math is covered by a golden test against IBGE's published 4.83%;
- **`expect`**: behavior instead of a number: say *"I don't have that"*, or explain why a question
  doesn't make sense.

A right number with no tool call counts as a **fail**: that's luck, not grounding.

```bash
pip install -e ".[evals]"
export ANTHROPIC_API_KEY=...
python -m bufunfa.evals.run
```

Results: *coming soon.*

## Getting started

```bash
git clone https://github.com/bonushealth/bufunfa.git
cd bufunfa
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

**Claude Code**

```bash
claude mcp add --transport stdio bufunfa -- bufunfa
```

**Claude Desktop** (`claude_desktop_config.json`; use the full path to the `bufunfa` executable
inside your virtual environment):

```json
{
  "mcpServers": {
    "bufunfa": { "command": "/path/to/bufunfa/.venv/bin/bufunfa" }
  }
}
```

## Project structure

```
bufunfa/
├── src/bufunfa/
│   ├── server.py           # MCP server and its five tools
│   ├── catalog.py          # curated series + search
│   ├── analysis.py         # the math (pure functions)
│   ├── service.py          # catalog -> cache -> API
│   ├── cache.py            # SQLite with TTL
│   ├── models.py           # Series, Observation, Kind, period parsing
│   ├── sources/bcb.py      # Banco Central SGS
│   ├── sources/ibge.py     # IBGE aggregates API (SIDRA)
│   └── evals/              # cases.toml, grading, runner
└── tests/                  # pytest, no network (httpx.MockTransport)
```

## Next

- More series: market expectations (Focus survey), unemployment (PNAD), GDP, regional IPCA.
- Streamable HTTP transport and a hosted public endpoint.
- Publish to PyPI and the MCP registry.
- An LLM judge for the behavioral eval cases.

## About the data

Banco Central data comes from the SGS API ([open data portal](https://dadosabertos.bcb.gov.br))
and is published under the Open Data Commons Open Database License (ODbL). IBGE data comes from the
[aggregates API](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3) (SIDRA).
bufunfa is an independent project, not affiliated with Banco Central or IBGE.

---

Built by [Fábio Augusto](https://github.com/bonushealth).
