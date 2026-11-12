# Issue 533: CII BR-IG / BR-IP variants tested at runtime

Context: [ConnectingEurope/eInvoicing-EN16931#533](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/533).
In `validation-1.3.17`, the CII binding swaps the IGIC (`L`) and IPSI (`M`) rule ids compared with UBL, and the CII IGIC rate rules reject a rate of 0.

**Modified work notice (EUPL 1.2, art. 5).** `patches/`, `xslt/V1/` and `xslt/V2/` are derived from the ConnectingEurope EN16931 validation artefacts `validation-1.3.17` and were modified on 8 Nov 2026. `xslt/BASE/` is the same tag rebuilt without any change. `probes/` are modified copies of two CEN examples from `fixtures/`. All of them stay under EUPL 1.2 (`../../LICENSE-EUPL-1.2.txt`, `../../NOTICE`).

## Variants

Both variants touch only `cii/schematron/CII/EN16931-CII-model.sch` and `cii/schematron/abstract/EN16931-CII-model.sch`. UBL is unchanged.

- **V1**: two-way rename `BR-IP-nn` ↔ `BR-IG-nn` (param names, assert ids, `$BR-…` references, message prefixes), done through unique temporary names, plus the current `BR-IP-06` / `BR-IP-07` (IGIC document-level allowance / charge rate) changed from `> 0` to `>= 0`.
- **V2**: V1 plus the current `BR-IP-05` (IGIC invoice-line rate) changed from `> 0` to `>= 0`, with its message aligned on the UBL text of the same rule.

Patches: `patches/V1.patch`, `patches/V2.patch` (`git diff` against the tag).

## Results

Full table: [`RESULTS.md`](RESULTS.md). Raw data: `RESULTS.json`.

- **Static check**: in V1 and V2, every `BR-IG-nn` message names IGIC and every `BR-IP-nn` message names IPSI, as in UBL (0 of 20 ids differ). In the published 1.3.17 CII, all 20 differ.
- **0 % IGIC**: V1 is not enough. On an all-IGIC invoice at rate 0, CII V1 still fails `BR-IG-05` (line rate `> 0`) while UBL accepts it. V2 accepts it, like UBL.
- **Rate boundaries**: with V2, rates 0 and 7 pass, and rates -1 and absent fail, at line level (`-05`) and on document allowances and charges (`-06`, `-07`), for both IGIC and IPSI. Apart from `-08` (next point), CII V2 fires the same BR-IG / BR-IP ids as UBL on every probe.
- **Remaining difference (not addressed by V1 or V2)**: on a line with rate -1 or no rate, UBL also fires `BR-IG-08` / `BR-IP-08` and CII never does. In CII, the `-08` rule context for `L` / `M` is the `ram:ApplicableTradeTax` element itself (`$VATAF`, `$VATAG`), so `../ram:RateApplicablePercent` selects nothing and the `every $rate in …` test is always true. The `S` rule (`$VATS`) uses the `ram:CategoryCode` element as context, where the same expression works. Upstream [555](https://github.com/ConnectingEurope/eInvoicing-EN16931/issues/555) (opened 11 Nov 2026, not from this repository) reports the same cause for CII `BR-IP-08` / `BR-IG-08`.
- **Non-regression**: on the 15 CII examples of the tag, the 9 CII fixtures of this repository and the 9 test documents of the upstream `test/cii` suite, V1 and V2 give exactly the same failed-assert list (id and location) as the published CII XSLT, and the upstream test expectations are met.

## Reproduce

Build (Java 17, Maven 3.9; uses the upstream `pom-preprocess.xml` and `pom-xslt-preprocessed.xml`, ph-schematron-maven-plugin 10.2.0):

```bash
variants/533/build.sh /tmp/w533           # writes patches/, xslt/ and xslt/SHA256SUMS
```

The rebuilt unpatched tag (`xslt/BASE`) differs from the published CII XSLT only by the 5-line licence header that upstream adds afterwards.

Probes and results (`saxonche==13.0.0`):

```bash
python3 variants/533/make_probes.py .
python3 variants/533/run_533.py --root . \
  --examples /tmp/w533/upstream/cii/examples --vefa /tmp/w533/upstream/test/cii --write
python3 variants/533/run_533.py --root . --check   # CI: replays probes and fixtures
```

Probes (`probes/cii`, `probes/ubl`, same mutation in both syntaxes): the CII base is `CII_business_example_Z.xml` (3 lines), the UBL base is `ubl-tc434-creditnote1.xml` (1 line). Each is first turned into a consistent all-`L` or all-`M` invoice at rate 0. Then one case is applied: line rate 0, 7 (VAT and totals recomputed), -1 or absent on the first line; or a document-level allowance and charge of 10.00 each at rate 0, 7, -1 or without rate (they cancel out, so totals stay consistent).
