# EN16931 validation oracles

[![Verify EN16931 oracle receipts](https://github.com/facturxapi/en16931-oracles/actions/workflows/verify-receipts.yml/badge.svg)](https://github.com/facturxapi/en16931-oracles/actions/workflows/verify-receipts.yml)

Reproducible machine verification of the official CEN EN16931 1.3.16
validation artefacts (ConnectingEurope eInvoicing-EN16931).

This repository publishes:

- the **10** official CEN example invoices used as oracles;
- the official **CII** and **UBL** XSLT from validation-1.3.16 (vendored, unmodified);
- SVRL receipts and a content-addressed `RESULTS.sha256`;
- intentional **mutants** that must fail;
- documented **GAPS** (blind spots) of the official Schematron/XSLT.

It does **not** claim anything about a commercial product, API, or runtime.

## Provenance and licences

| Object | Licence |
|---|---|
| Official XML fixtures + XSLT | **EUPL 1.2** (ConnectingEurope / validation-1.3.16), unmodified copies |
| Attribution | See `NOTICE` |
| Licence notes | See `LICENSE-NOTES.md` and `LICENSE-EUPL-1.2.txt` |

Oracle prose under `oracles/*.md` describes the machine-verified candidate status of each fixture.

## Reproduce

From the repository root:

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt && .venv/bin/python scripts/validate.py
```

- Default (`--mode reference`): vendored XSLT under `vendor/en16931-1.3.16/` + SaxonC-HE 13.0.
- Mutants: `.venv/bin/python scripts/validate.py --dir mutants --no-expected` (expect failed-assert on each file).

Expected reference hash (also in `oracles/receipts/RESULTS.sha256`):

```
dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab  RESULTS.json
```

## Fixtures (reference oracles)

| File | Syntax | Expected |
|---|---|---|
| `CII-BR-CO-10-RoundingIssue.xml` | CII | 0 failed-assert |
| `CII_business_example_01.xml` | CII | 0 failed-assert |
| `CII_business_example_02.xml` | CII | 0 failed-assert |
| `CII_business_example_Z.xml` | CII | 0 failed-assert |
| `CII_example1.xml` | CII | 0 failed-assert |
| `CII_example3.xml` | CII | 0 failed-assert |
| `CII_example5.xml` | CII | 0 failed-assert |
| `XRechnung-O.xml` | CII | 0 failed-assert |
| `huf_example_cii.xml` | CII | 0 failed-assert |
| `ubl-tc434-creditnote1.xml` | UBL | 0 failed-assert |

`XRechnung-O.xml` is an official EN16931 category-O CII example; it is **not** a CIUS XRechnung conformity claim.

## Out of scope

- Factur-X 1.09.2 / ZUGFeRD product profiles
- BR-FR / CTC-FR
- Product quality, commercial APIs, or performance benchmarks

## Layout

- `fixtures/` — official examples
- `oracles/` — candidate notes + SVRL receipts
- `mutants/` — intentional failures
- `gaps/` — documented blind spots
- `vendor/en16931-1.3.16/` — official XSLT
- `scripts/validate.py` — reproducible runner

## BR-FR Flux2 pack (`brfr/`)

French Flux2 (France_RFE) dual-version fixtures, mutants, gaps, and receipts.
See `brfr/README.md` and the BR-FR section of `LICENSE-NOTES.md`.
