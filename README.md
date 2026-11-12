# EN 16931 validation oracles

[![Verify EN16931 oracle receipts](https://github.com/facturxapi/en16931-oracles/actions/workflows/verify-receipts.yml/badge.svg)](https://github.com/facturxapi/en16931-oracles/actions/workflows/verify-receipts.yml) [![EN16931 upstream drift](https://github.com/facturxapi/en16931-oracles/actions/workflows/upstream-drift.yml/badge.svg)](https://github.com/facturxapi/en16931-oracles/actions/workflows/upstream-drift.yml)

Upgrading to EN 16931 validation [1.3.17](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.17)? Some behaviour changes are not in the release notes. Each one below is a one-line probe with its SVRL receipt, replayable in one command.

| Change in 1.3.17 | Effect | Probe | Upstream (state read 11 Nov 2026) |
|---|---|---|---|
| Greek VAT prefix `EL` now fails `BR-CO-09` (CII and UBL). The list was aligned for #509; the assert text still says Greece may use `EL`. | Seller VAT id (BT-31) `EL…`: 0 failed-assert in 1.3.16, 1 fatal `BR-CO-09` in 1.3.17 | `gaps/CII_example1-bt31-EL.xml`, `gaps/ubl-tc434-creditnote1-bt31-EL.xml` | [532](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/532), open; reproduced here |
| IGIC / IPSI rules renamed from `BR-AF-*` / `BR-AG-*` (#519) in opposite directions: IGIC is `BR-IP-*` in CII and `BR-IG-*` in UBL, IPSI the reverse. | Same one-line defect, a different rule id per syntax | `gaps/*-bt151-L.xml`, `gaps/*-bt151-M.xml`, [`variants/533/`](variants/533/README.md) | [533](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/533), open; reproduced here |
| Fixed upstream in 1.3.17: BT-159 country `AN` / `SS` (CII now rejects `AN` and accepts `SS`), BT-21 subject `BAT` (UBL now accepts it), UBL `BR-CO-09` single letter `A` (now rejected) | 4 probes change verdict between 1.3.16 and 1.3.17 | `gaps/*-bt159-origin-AN.xml` / `-SS.xml`, `gaps/*-bt21-*BAT*.xml`, `gaps/ubl-tc434-creditnote1-bt31-A.xml` | [509](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/509), [510](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/510) closed, reproduced here; [515](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/515) closed, reported from here |

Reported from this repository: [515](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/515) (UBL `BR-CO-09` accepted a single letter `A`) was fixed in 1.3.17. [516](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/516) (`CII-DT-097` accepts calendar-impossible dates such as `20260231`, FINDING 3 in [`GAPS.md`](GAPS.md)) is labelled "Forwarded to CEN/TC434" upstream and still open (read 12 Nov 2026).

Use it to: check a validator upgrade before you ship it · run the probes against your own validator · cite a reproducible receipt in an upstream issue.

Scope: this repository runs the vendored, unmodified ConnectingEurope EN 16931 validation-1.3.17 XSLT (and, in `brfr/`, the France_RFE Flux2 XSLT `v1.4.0.02`, `v1.4.0.03` and `v1.4.0.04`; in `variants/533/`, two patched CII builds) with SaxonC-HE 13.0 on the files it contains, and states nothing about Factur-X / ZUGFeRD profile rulesets, other validators or commercial products.

Maintained by FacturX API — https://facturxapi.com

## Replay

From the repository root:

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/validate.py                                                     # 10 fixtures, compared to scripts/expected.json
.venv/bin/python scripts/validate.py --dir gaps --out-dir gaps/receipts --no-expected     # 36 gaps probes
.venv/bin/python scripts/validate.py --dir mutants --out-dir mutants/receipts --no-expected  # 10 mutants, each must fail
git diff --exit-code                                                                      # receipts are byte-stable
```

CI runs the same replays plus `scripts/verify_receipts.py`, `scripts/verify_gaps_receipts.py`, `scripts/check_brcl08_polarity.py`, `variants/533/run_533.py --check` and the unit tests in `tests/` ([workflow](.github/workflows/verify-receipts.yml)).

Expected hashes:

```
7f812b376356c1ac3ab10b119d69c5e0c1f5b866b8914b08fe51132e60398c6d  oracles/receipts/RESULTS.json
2c32ab6c3da8a6f3943457192cc63b8f82770af9846abcbde077c74f07ad1125  gaps/receipts/RESULTS.json
```

## Run it on your own files

```bash
.venv/bin/python scripts/validate.py --dir /path/to/invoices --out-dir /tmp/en16931-receipts --no-expected
```

- The syntax is chosen from the file name: names starting with `ubl-` run the UBL XSLT, all others run the CII XSLT.
- Always pass `--out-dir`: without it, receipts are written to `oracles/receipts/`.
- Each file gets a `.svrl.xml` and a `.receipt.md`, plus a `RESULTS.json` / `RESULTS.sha256` for the set.

In CI, [validate-einvoice](https://github.com/facturxapi/validate-einvoice) is a GitHub Action that runs the same ConnectingEurope XSLT (1.3.16 by default, 1.3.17 with `version: '1.3.17'`).

## `gaps/`: one-line probes with receipts

Each probe is a copy of a CEN example with one line changed, replayed on the 1.3.17 XSLT, with its SVRL receipt in `gaps/receipts/`. The 36 probes, by state in 1.3.17:

| State in 1.3.17 | Probes | What it means |
|---|---:|---|
| Open | 14 | 8 cases where a rule's text covers the value but its test lets it through (BR-CO-09, CII-DT-097, BR-DEC-13), 4 IGIC / IPSI probes (533), 2 `EL` probes (532) |
| Fixed in 1.3.17 | 8 | probes for 509 (4), 510 (3) and 515 (1) |
| Observation | 8 | 0 failed-assert, and no rule claims to test the case |
| Control | 6 | a rule fires as expected (5), or a valid neighbour passes (1) |

Two more files in `gaps/engine-errors/` make Saxon stop before any SVRL (`FORG0001`). The four UBL probes for 509 / 510 derive from the official UBL example 5, which is not in `fixtures/`. Full table, rule texts and counter-tests: [`GAPS.md`](GAPS.md) (English summary on top, details in French).

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

`XRechnung-O.xml` is an official EN 16931 category-O CII example, not an XRechnung CIUS conformity claim.

## Licences

Decision of 11 Nov 2026. Attribution: FacturX API (facturxapi.com).

| Content | Licence |
|---|---|
| Unmodified ConnectingEurope files (`fixtures/`, `vendor/en16931-*`) | EUPL-1.2 (upstream, unchanged) |
| Probes, mutants and variants (`gaps/`, `mutants/`, `variants/533/`): modified copies of CEN examples and artefacts | EUPL-1.2 (derivative works, art. 5) |
| Our scripts, tests, workflows, receipts and `RESULTS` files | EUPL-1.2 |
| Prose: `README.md`, `GAPS.md`, `oracles/*.md` and other notes | CC-BY-4.0 |
| `brfr/vendor/` (unmodified France_RFE files) | Apache-2.0 (upstream, unchanged) |

Texts: [`LICENSE`](LICENSE) (EUPL-1.2), [`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt), [`brfr/vendor/LICENSE-APACHE-2.0-France_RFE.txt`](brfr/vendor/LICENSE-APACHE-2.0-France_RFE.txt). Attributions: [`NOTICE`](NOTICE). Details: [`LICENSE-NOTES.md`](LICENSE-NOTES.md).

## Layout

- `fixtures/` — 10 official ConnectingEurope examples (unmodified)
- `vendor/en16931-1.3.17/` — official CII and UBL XSLT (unmodified)
- `oracles/` — per-fixture notes and SVRL receipts
- `mutants/` — 10 one-line mutants that must fail ([`MUTANTS.md`](MUTANTS.md))
- `gaps/` — one-line probes with receipts ([`GAPS.md`](GAPS.md))
- `variants/533/` — CII fixes V1 / V2 for upstream issue 533, tested at runtime
- `mapping/` — rule-id mapping proof, measured on 1.3.16 ([`MAPPING-PROOF.md`](MAPPING-PROOF.md))
- `brfr/` — France_RFE Flux2 pack, `v1.4.0.02`, `v1.4.0.03` and `v1.4.0.04` ([`brfr/README.md`](brfr/README.md))
- `scripts/` — runner and CI checks ([`scripts/README.md`](scripts/README.md))
- `tests/` — unit tests for the CI checks

## See also

- [validate-einvoice](https://github.com/facturxapi/validate-einvoice) — GitHub Action running the official ConnectingEurope XSLT on CII / UBL files.
- [awesome-einvoicing](https://github.com/facturxapi/awesome-einvoicing) — sourced map of specs, validators, libraries and corpora.

## Changelog

- **11 Nov 2026** — licence decision: EUPL-1.2 for code, data and receipts, CC-BY-4.0 for prose (see Licences); root `LICENSE` and `LICENSE-CC-BY-4.0.txt` added.
- **11 Nov 2026** — `brfr/`: France_RFE `v1.4.0.04` replayed (artefacts, receipts, 24 probes), PR #16.
- **10 Nov 2026** — two `EL` probes for upstream issue 532 (`gaps/`, 34 → 36 probes), PR #15.
- **8 Nov 2026** — `variants/533/`: CII fixes V1 / V2 for upstream issue 533 tested at runtime, PR #14.
- **18 Oct 2026** — four IGIC / IPSI probes for upstream issue 533 (`gaps/*-bt151-L/M`), PR #11.
- **18 Oct 2026** — updated to [validation-1.3.17](https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/tag/validation-1.3.17). The 10 fixtures stay at 0 failed-assert and the 10 mutants fail on the same rule ids. `CII_example3.xml` is the new 1.3.17 copy (one `SpecifiedTradeSettlementPaymentMeans` block removed upstream); the other 9 fixtures are byte-identical to 1.3.16. Upstream renamed the IGIC rules `BR-AF-*` and the IPSI rules `BR-AG-*` (#519), but not the same way in both syntaxes: IGIC became `BR-IP-*` in CII and `BR-IG-*` in UBL, IPSI the reverse (measured by matching rule texts across the two vendored XSLT). No fixture or mutant cites those ids. Four `gaps/` probes changed verdict because upstream fixed #509, #510 and #515: see `GAPS.md`.
