# Lab 6 - Vending Machine: Code and Branch Coverage

**Name:** Paturu Naga Jignas

**USN:** PES2UG24AM110

## Aim

Test the supplied vending machine module and achieve the requested 90-100%
coverage. The completed suite achieves **100% statement and branch coverage**.

## Files

| File | Purpose |
| --- | --- |
| `vending_machine.py` | Supplied item selection, change-making and purchase logic |
| `test_vending_machine.py` | 41 pytest cases, including parameterized cases |
| `requirements.txt` | Test and coverage dependencies |
| `coverage_report.txt` | Recorded validation output |

## Run

From the repository root:

```shell
cd lab6
python -m pip install -r requirements.txt
python -m coverage run --branch --source=vending_machine -m pytest -q
python -m coverage report -m --fail-under=100
```

The last command exits with a failure status if combined statement and branch
coverage drops below 100%. To generate an interactive source report, run
`python -m coverage html` and open `htmlcov/index.html`.

## Test cases

Amounts are in the same integer units used by the supplied module: cola costs
150, chips cost 100 and candy costs 75. Available coin denominations are
100, 50, 25, 10 and 5.

| Area | Cases | Scenarios and assertions |
| --- | ---: | --- |
| Item selection | 10 | Invalid item; missing or zero stock; credit one unit below each price; exact payment for all items; excess credit; unchanged stock |
| Change-making | 16 | Zero; two negative amounts raising `ValueError`; each coin denomination; mixed and repeated coins; amounts with an unrepresentable remainder |
| Purchases | 15 | Invalid, sold-out and insufficient-credit failures; inexact change with and without a partially formed coin list; unchanged stock on failure; exact and excess payments; decrementing only the selected item; last-unit and repeated purchases until sold out |
| **Total** | **41** | **All cases passed** |

## Coverage result

| Module | Statements | Missed statements | Branches | Partial branches | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: |
| `vending_machine.py` | 30 | 0 | 18 | 0 | **100%** |

The suite exercises both outcomes of every selection and purchase decision,
the negative and non-negative change paths, loop entry and exit, and both
representable and unrepresentable change results. Assertions check returned
values, exception messages and stock mutations.

The original `vending_machine.py` is unchanged. Full coverage describes the
executed paths in this module; these tests verify its supplied behavior.
