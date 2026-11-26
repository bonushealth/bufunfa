"""Eval runner: put a real agent in front of bufunfa and grade its answers.

    python -m bufunfa.evals.run                 # all cases
    python -m bufunfa.evals.run --case ipca-2024
    BUFUNFA_EVAL_MODEL=claude-sonnet-5-5 python -m bufunfa.evals.run

Needs ANTHROPIC_API_KEY (pip install -e ".[evals]"). Hits the real BCB/IBGE APIs,
through the cache. Roadmap step 8.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

CASES_PATH = Path(__file__).with_name("cases.toml")
DEFAULT_MODEL = os.getenv("BUFUNFA_EVAL_MODEL", "claude-haiku-5-5")
MAX_TURNS = 8


@dataclass
class AgentResult:
    answer: str
    tool_calls: list[str] = field(default_factory=list)  # tool names, in order
    tool_errors: int = 0


@dataclass
class Grade:
    case_id: str
    passed: bool
    expected: float | str | None
    got: float | None
    reason: str


def load_cases(path: Path = CASES_PATH) -> list[dict]:
    with path.open("rb") as file:
        return tomllib.load(file)["case"]


async def ask_agent(question: str, model: str = DEFAULT_MODEL) -> AgentResult:
    """Run one question through Claude with bufunfa's tools, the way Claude Code would."""
    # TODO: start the server over stdio:
    #         async with mcp.Client(mcp.StdioServerParameters(command="bufunfa")) as client:
    # TODO: tools = (await client.list_tools()).tools ->
    #         [{"name": t.name, "description": t.description, "input_schema": t.input_schema}]
    # TODO: loop up to MAX_TURNS: anthropic.AsyncAnthropic().messages.create(model=..., tools=...,
    #         system=<the server's instructions>, messages=...)
    #       for every tool_use block: client.call_tool(name, input) -> a tool_result block
    #       (send is_error back too: recovering from errors is part of what you're testing)
    #       stop when stop_reason != "tool_use"; the last text block is the answer.
    raise NotImplementedError


async def expected_value(case: dict) -> float | str | None:
    """`expected` as is; `expected_from` by calling that tool directly; `expect` as the label."""
    # TODO: for expected_from, call the tool through an MCP client too (same code path as the
    #       agent) and read case["expected_from"]["field"] from the JSON result.
    raise NotImplementedError


def grade(case: dict, expected: float | str | None, result: AgentResult) -> Grade:
    """Numbers: within tolerance AND at least one tool call (a right number from memory fails).

    "no_data": no number in the answer, or an explicit "não tenho / not available".
    "refuse_or_redirect": mentions that it's an annual rate, or used selic_diaria.
    """
    # TODO: use grading.extract_number / grading.within_tolerance.
    # Later: an LLM judge for the behavioral cases, once keyword checks start lying to you.
    raise NotImplementedError


def main() -> None:
    # TODO: argparse (--case, --model); run every case; print a table:
    #       id | expected | got | pass | tools used ; then accuracy.
    # TODO: exit code 1 when accuracy drops below a threshold -> usable in CI later.
    raise NotImplementedError


if __name__ == "__main__":
    main()
