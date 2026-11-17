"""Lab 6: Code and Branch Coverage.

Name: Paturu Naga Jignas
USN: PES2UG24AM110
"""

import pytest

from vending_machine import make_change, purchase, select_item


def test_invalid_item():
    assert select_item("water", {}, 100) == "invalid"


@pytest.mark.parametrize(
    "item, stock, credit, expected",
    [
        pytest.param("cola", {}, 150, "sold_out", id="missing-stock"),
        pytest.param("chips", {"chips": 0}, 100, "sold_out", id="zero-stock"),
        pytest.param("cola", {"cola": 1}, 149, "insufficient", id="cola-short"),
        pytest.param("chips", {"chips": 1}, 99, "insufficient", id="chips-short"),
        pytest.param("candy", {"candy": 1}, 74, "insufficient", id="candy-short"),
        pytest.param("cola", {"cola": 1}, 150, "ok", id="cola-exact"),
        pytest.param("chips", {"chips": 1}, 100, "ok", id="chips-exact"),
        pytest.param("candy", {"candy": 1}, 75, "ok", id="candy-exact"),
        pytest.param("cola", {"cola": 2}, 200, "ok", id="extra-credit"),
    ],
)
def test_select_item(item, stock, credit, expected):
    original_stock = stock.copy()

    assert select_item(item, stock, credit) == expected
    assert stock == original_stock


def test_no_change_needed():
    assert make_change(0) == []


@pytest.mark.parametrize("amount", [-1, -100])
def test_negative_change(amount):
    with pytest.raises(ValueError, match="^negative amount$"):
        make_change(amount)


@pytest.mark.parametrize(
    "amount, expected",
    [
        (5, [5]),
        (10, [10]),
        (25, [25]),
        (50, [50]),
        (100, [100]),
        (190, [100, 50, 25, 10, 5]),
        (200, [100, 100]),
        (285, [100, 100, 50, 25, 10]),
    ],
)
def test_exact_change(amount, expected):
    assert make_change(amount) == expected


@pytest.mark.parametrize("amount", [1, 4, 6, 76, 101])
def test_change_with_unrepresentable_remainder(amount):
    assert make_change(amount) is None


@pytest.mark.parametrize(
    "item, stock, credit, expected",
    [
        pytest.param("water", {"water": 1}, 100, "invalid", id="invalid-item"),
        pytest.param("cola", {}, 150, "sold_out", id="missing-stock"),
        pytest.param("chips", {"chips": 0}, 100, "sold_out", id="zero-stock"),
        pytest.param("cola", {"cola": 1}, 149, "insufficient", id="cola-short"),
        pytest.param("chips", {"chips": 1}, 99, "insufficient", id="chips-short"),
        pytest.param("candy", {"candy": 1}, 74, "insufficient", id="candy-short"),
        pytest.param("candy", {"candy": 1}, 76, "no_exact_change", id="remainder-only"),
        pytest.param("cola", {"cola": 1}, 251, "no_exact_change", id="coin-and-remainder"),
    ],
)
def test_rejected_purchase_preserves_stock(item, stock, credit, expected):
    original_stock = stock.copy()

    assert purchase(item, stock, credit) == (expected, [])
    assert stock == original_stock


@pytest.mark.parametrize(
    "item, quantity, credit, expected_change",
    [
        pytest.param("cola", 2, 150, [], id="cola-exact"),
        pytest.param("chips", 1, 100, [], id="chips-last-unit"),
        pytest.param("candy", 1, 75, [], id="candy-last-unit"),
        pytest.param("cola", 2, 340, [100, 50, 25, 10, 5], id="all-coins"),
        pytest.param("chips", 2, 300, [100, 100], id="repeated-coin"),
        pytest.param("candy", 2, 150, [50, 25], id="mixed-change"),
    ],
)
def test_successful_purchase_updates_only_selected_stock(
    item, quantity, credit, expected_change
):
    stock = {"cola": 3, "chips": 4, "candy": 5}
    stock[item] = quantity
    expected_stock = stock.copy()
    expected_stock[item] -= 1

    assert purchase(item, stock, credit) == ("dispensed", expected_change)
    assert stock == expected_stock


def test_repeated_purchases_until_sold_out():
    stock = {"cola": 2, "chips": 3}

    assert purchase("cola", stock, 150) == ("dispensed", [])
    assert stock == {"cola": 1, "chips": 3}
    assert purchase("cola", stock, 200) == ("dispensed", [50])
    assert stock == {"cola": 0, "chips": 3}
    assert purchase("cola", stock, 200) == ("sold_out", [])
    assert stock == {"cola": 0, "chips": 3}
