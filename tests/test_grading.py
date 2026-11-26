"""Contract for bufunfa.evals.grading: reading a number out of a pt-BR (or English) answer."""

import pytest

from bufunfa.evals.grading import extract_number, within_tolerance


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        ("A inflação acumulada em 2024 foi de 4,83%.", 4.83),
        ("Inflation in 2024 was 4.83%.", 4.83),
        ("O mínimo foi de R$ 1.412,00 pra R$ 1.518,00, alta de 7,51 %.", 7.51),
        ("Ganho real de -2,1% em relação aos alimentos.", -2.1),
        ("O valor corrigido é R$ 1.518,00", 1518.0),
    ],
)
def test_extract_number(answer, expected):
    assert extract_number(answer) == pytest.approx(expected)


def test_extract_number_without_numbers():
    assert extract_number("Não tenho esse dado no bufunfa.") is None


def test_within_tolerance():
    assert within_tolerance(4.83, 4.8313, 0.01)
    assert not within_tolerance(4.8, 4.83, 0.01)
    assert not within_tolerance(None, 4.83, 0.01)
