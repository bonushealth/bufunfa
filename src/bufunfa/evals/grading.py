"""Pure helpers to grade an agent's answer. No LLM, no network.

Contract: tests/test_grading.py
"""

from __future__ import annotations


def extract_number(text: str) -> float | None:
    """The number the answer commits to: the first one followed by %, else the last number."""
    # TODO: regex for numbers in both styles: "4,83" / "4.83" / "-2,1" / "1.518,00" (pt-BR
    #       thousands). Prefer a number followed by "%"; otherwise the last number; none -> None.
    # Pegadinha: "1.518" is one thousand five hundred in pt-BR, not one point five.
    raise NotImplementedError


def within_tolerance(got: float | None, expected: float, tolerance: float) -> bool:
    # TODO: None is never within tolerance.
    raise NotImplementedError
