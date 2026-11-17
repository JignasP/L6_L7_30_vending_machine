"""Lab 7: Fuzz Testing.

Name: Paturu Naga Jignas
USN: PES2UG24AM110
"""

from pathlib import Path
import re
import runpy

import pytest
from hypothesis import given, settings, strategies as st

import vending_machine
from vending_machine import change_due, parse_coins, slot_position


FUZZ_SETTINGS = settings(
    max_examples=500,
    derandomize=True,
    database=None,
    deadline=None,
    report_multiple_bugs=False,
)


@FUZZ_SETTINGS
@given(st.text() | st.none())
def test_parse_coins_no_crash(s):
    result = parse_coins(s)
    assert result is None or (
        isinstance(result, list) and all(isinstance(coin, int) for coin in result)
    )


@FUZZ_SETTINGS
@given(st.text() | st.none())
def test_slot_position_no_crash(s):
    result = slot_position(s)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and all(isinstance(value, int) for value in result)
        and 0 <= result[0] < 26
        and result[1] >= 0
    )


@FUZZ_SETTINGS
@given(st.text() | st.none())
def test_change_due_no_crash(s):
    result = change_due(s)
    assert result is None or (
        isinstance(result, str) and re.fullmatch(r"[0-9]+ five-coins", result)
    )


@FUZZ_SETTINGS
@given(st.lists(st.integers(-10**9, 10**9), min_size=1, max_size=50))
def test_parse_coins_round_trip(coins):
    csv = ",".join(f" {coin} " for coin in coins)
    assert parse_coins(csv) == coins


@FUZZ_SETTINGS
@given(
    row=st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
    column=st.integers(min_value=1, max_value=10000),
)
def test_slot_position_round_trip(row, column):
    assert slot_position(f"{row}{column}") == (ord(row.upper()) - ord("A"), column - 1)


@FUZZ_SETTINGS
@given(
    price=st.integers(min_value=0, max_value=10**9),
    five_coins=st.integers(min_value=0, max_value=10**6),
)
def test_exact_change(price, five_coins):
    paid = price + five_coins * 5
    assert change_due(f"{paid}/{price}") == f"{five_coins} five-coins"


@FUZZ_SETTINGS
@given(
    price=st.integers(min_value=1, max_value=10**9),
    shortfall=st.integers(min_value=1, max_value=10**9),
)
def test_underpayment_is_rejected(price, shortfall):
    assert change_due(f"{price - shortfall}/{price}") is None


@FUZZ_SETTINGS
@given(
    price=st.integers(min_value=0, max_value=10**9),
    five_coins=st.integers(min_value=0, max_value=10**6),
    remainder=st.integers(min_value=1, max_value=4),
)
def test_inexact_change_is_rejected(price, five_coins, remainder):
    paid = price + five_coins * 5 + remainder
    assert change_due(f"{paid}/{price}") is None


@pytest.mark.parametrize(
    "value", [None, "", " ", "5,", "5,,10", "five,10", "5.5,10", "5\x00,10"]
)
def test_invalid_coin_csv(value):
    assert parse_coins(value) is None


@pytest.mark.parametrize(
    "value", [None, "", "A", "AA1", "A0", "A-1", "@1", "\u00df1", "\ufb061", "A1x"]
)
def test_invalid_slot_code(value):
    assert slot_position(value) is None


@pytest.mark.parametrize(
    "value",
    [None, "", "200", "200/150/0", "two/150", "200/one", "149/150", "-5/0", "200/-5", "151/150"],
)
def test_invalid_payment(value):
    assert change_due(value) is None


@pytest.mark.parametrize("function", [parse_coins, slot_position, change_due])
@pytest.mark.parametrize("value", [0, [], {}, b"5,10"])
def test_non_text_input(function, value):
    assert function(value) is None


@pytest.mark.parametrize(
    "as_script, entries, expected",
    [
        (
            False,
            ("5,10,25", "B7", "200/150"),
            ("Coins: [5, 10, 25]", "Row and Column: (1, 6)", "Change Due: 10 five-coins"),
        ),
        (
            True,
            ("bad", "\u00df1", "oops"),
            ("Coins: None", "Row and Column: None", "Change Due: None"),
        ),
    ],
)
def test_cli(as_script, entries, expected, monkeypatch, capsys):
    answers = iter(entries)
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    if as_script:
        runpy.run_path(str(Path(vending_machine.__file__)), run_name="__main__")
    else:
        vending_machine.main()
    output = capsys.readouterr().out
    for text in expected:
        assert text in output
