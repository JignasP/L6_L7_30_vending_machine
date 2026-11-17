# Lab 7 - Vending Machine: Fuzz Testing

**Name:** Paturu Naga Jignas

**USN:** PES2UG24AM110

## Aim

Use Hypothesis to generate inputs for the three vending-machine helpers,
reproduce failures, fix input handling, and retain regression tests.

## Files

| File | Purpose |
| --- | --- |
| `vending_machine.py` | Validated input helpers and the interactive demonstration |
| `test_vending_machine.py` | Eight Hypothesis properties and 42 focused test cases |
| `requirements.txt` | Test and coverage dependencies |
| `fuzz_test_report.txt` | Before/after findings and recorded test statistics |

## Run

Run each lab from its own folder. From the repository root:

```shell
cd lab7
python -m pip install -r requirements.txt
python -m pytest -q --hypothesis-show-statistics
```

To also collect statement and branch coverage:

```shell
python -m coverage run --branch --source=vending_machine -m pytest -q --hypothesis-show-statistics
python -m coverage report -m --fail-under=100
```

For the interactive demonstration, run `python vending_machine.py`.

## Input handling

Malformed input returns `None`. Valid inputs retain the original result formats.

| Helper | Valid example | Result | Validation |
| --- | --- | --- | --- |
| `parse_coins` | `5,10,25` | `[5, 10, 25]` | A string containing comma-separated integer tokens; whitespace and signed integers are supported |
| `slot_position` | `B7` or `b7` | `(1, 6)` | An A-Z row, case insensitive, followed by a positive integer column; coordinates are zero based |
| `change_due` | `200/150` | `10 five-coins` | Exactly two integer amounts; payment and price are nonnegative, payment covers the price, and the difference is divisible by five |

## Findings and fixes

The first fuzz run failed all three no-crash properties. Hypothesis reduced each
failure to `None`: `parse_coins` and `change_due` raised `AttributeError`, while
`slot_position` raised `TypeError`.

The fixes check input types before using string operations, handle failed integer
conversions, validate row and column values, and reject negative payments,
underpayment and inexact five-unit change. Targeted regression cases also cover
empty strings, missing and extra separators, invalid numbers, zero and negative
columns, and Unicode characters whose uppercase form contains multiple letters.

The properties verify arbitrary Unicode strings and `None`, valid coin-list and
slot round trips, exact change, underpayment and inexact change. The focused
cases also test other non-string types and both CLI execution paths.

## Verified results

Each property uses `max_examples=500`, `derandomize=True`, `database=None` and
`deadline=None`. Hypothesis reports **500 passing examples for each of eight
properties**, for **4,000 passing generated examples**. The complete suite has
**50 passing tests**: eight property tests and 42 focused cases.

| Module | Statements | Missed statements | Branches | Partial branches | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: |
| `vending_machine.py` | 49 | 0 | 18 | 0 | **100%** |

Validated with Python 3.10.8, pytest 9.0.3, Hypothesis 6.112.1 and coverage.py
7.6.1. Lab 6 was also rerun separately: all **41 tests passed**.
