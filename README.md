# EN16931 validation oracles

[![Verify EN16931 oracle receipts](https://github.com/facturxapi/en16931-oracles/actions/workflows/verify-receipts.yml/badge.svg)](https://github.com/facturxapi/en16931-oracles/actions/workflows/verify-receipts.yml) [![EN16931 upstream drift](https://github.com/facturxapi/en16931-oracles/actions/workflows/upstream-drift.yml/badge.svg)](https://github.com/facturxapi/en16931-oracles/actions/workflows/upstream-drift.yml)

Reproducible machine verification of the official ConnectingEurope
EN16931 1.3.16 validation artefacts (`eInvoicing-EN16931`).

This repository publishes:

- the **10** official ConnectingEurope example invoices used as oracles;
- the official **CII** and **UBL** XSLT from validation-1.3.16 (vendored, unmodified);
- SVRL receipts and a content-addressed `RESULTS.sha256`;
- intentional **mutants** that must fail.

It does **not** claim anything about a commercial product, API, or runtime.

## Which FacturX repo should I use?

- [validate-einvoice](https://github.com/facturxapi/validate-einvoice) — GitHub Action that runs the official ConnectingEurope EN16931 1.3.16 XSLT artefacts (CII/UBL).
- [en16931-oracles](https://github.com/facturxapi/en16931-oracles) — Replayable fixtures, receipts and mutants for that same 1.3.16 pin.
- [awesome-einvoicing](https://github.com/facturxapi/awesome-einvoicing) — Sourced map of specs, validators, libraries and corpora. Inclusion is not a ranking.

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
- `gaps/` — extra fixtures (notes only; not a published findings list)
- `vendor/en16931-1.3.16/` — official XSLT
- `scripts/validate.py` — reproducible runner

## See also

- Why two validators can return different verdicts on the same XML (ITB 16/16 on this corpus, FNFE-MPE V1.4.0 calendar of 30 June 2026): https://facturxapi.com/blog/pourquoi-deux-validateurs-divergent
- GitHub Action that runs the same official ConnectingEurope 1.3.16 XSLT artefacts: https://github.com/facturxapi/validate-einvoice
- Sourced map of the European e-invoicing ecosystem: https://github.com/facturxapi/awesome-einvoicing

## BR-FR Flux2 pack (`brfr/`)

French Flux2 (France_RFE) dual-version fixtures, mutants, gaps, and receipts.
See `brfr/README.md` and the BR-FR section of `LICENSE-NOTES.md`.
