#!/usr/bin/env python3
"""Generate the issue 533 probes from two pinned CEN fixtures.

CII base: fixtures/CII_business_example_Z.xml (3 lines + 1 VAT breakdown, all Z at 0.00).
UBL base: fixtures/ubl-tc434-creditnote1.xml (1 line + 1 VAT breakdown, E at 0.00).

Every probe is first turned into a consistent all-L (IGIC) or all-M (IPSI) document at
rate 0 (all category codes switched, UBL exemption reason removed), then one case:

  line-0       nothing else (line and breakdown rates 0)
  line-7       every rate set to 7 and the VAT and totals recomputed (consistent)
  line-neg     first invoice line rate set to -1.00 (breakdown untouched)
  line-absent  first invoice line rate removed (breakdown untouched)
  doc-0        a document-level allowance and a charge of 10.00 each, same category, rate 0
  doc-7        same, rate 7
  doc-neg      same, rate -1.00
  doc-absent   same, no rate

The allowance and the charge cancel out, so totals and the breakdown stay unchanged.
Edits are literal string replacements with an exact expected count. Writes under
variants/533/probes/. Usage: make_probes.py [repo-root]
"""

from __future__ import annotations

import sys
from pathlib import Path

CATEGORIES = ("L", "M")
CASES = ("line-0", "line-7", "line-neg", "line-absent", "doc-0", "doc-7", "doc-neg", "doc-absent")


def sub(text: str, old: str, new: str, count: int, label: str) -> str:
    found = text.count(old)
    if found != count:
        raise SystemExit(f"{label}: expected {count} x {old!r}, found {found}")
    return text.replace(old, new)


def sub_first(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"{label}: {old!r} not found")
    return text.replace(old, new, 1)


# ---------------------------------------------------------------- CII

CII_RATE0 = "<ram:RateApplicablePercent>0.00</ram:RateApplicablePercent>"


def cii_doc_block(cat: str, rate: str | None) -> str:
    rate_xml = (
        f"\n            <ram:RateApplicablePercent>{rate}</ram:RateApplicablePercent>" if rate is not None else ""
    )
    out = ""
    for indicator, reason in (("false", "Discount"), ("true", "Freight")):
        out += (
            "<ram:SpecifiedTradeAllowanceCharge>\n"
            f"          <ram:ChargeIndicator><udt:Indicator>{indicator}</udt:Indicator></ram:ChargeIndicator>\n"
            "          <ram:ActualAmount>10.00</ram:ActualAmount>\n"
            f"          <ram:Reason>{reason}</ram:Reason>\n"
            "          <ram:CategoryTradeTax>\n"
            "            <ram:TypeCode>VAT</ram:TypeCode>\n"
            f"            <ram:CategoryCode>{cat}</ram:CategoryCode>{rate_xml}\n"
            "          </ram:CategoryTradeTax>\n"
            "        </ram:SpecifiedTradeAllowanceCharge>\n"
            "      "
        )
    return out


def cii_probe(base: str, cat: str, case: str) -> str:
    t = sub(base, "<ram:CategoryCode>Z</ram:CategoryCode>", f"<ram:CategoryCode>{cat}</ram:CategoryCode>", 4, "cii category")
    if case == "line-7":
        t = sub(t, CII_RATE0, "<ram:RateApplicablePercent>7.00</ram:RateApplicablePercent>", 4, "cii rates")
        t = sub(t, "<ram:CalculatedAmount>0.00</ram:CalculatedAmount>", "<ram:CalculatedAmount>818.57</ram:CalculatedAmount>", 1, "cii vat")
        t = sub(t, '<ram:TaxTotalAmount currencyID="EUR">0.0</ram:TaxTotalAmount>', '<ram:TaxTotalAmount currencyID="EUR">818.57</ram:TaxTotalAmount>', 1, "cii tax total")
        t = sub(t, "<ram:GrandTotalAmount>11693.87</ram:GrandTotalAmount>", "<ram:GrandTotalAmount>12512.44</ram:GrandTotalAmount>", 1, "cii grand")
        t = sub(t, "<ram:DuePayableAmount>11693.87</ram:DuePayableAmount>", "<ram:DuePayableAmount>12512.44</ram:DuePayableAmount>", 1, "cii due")
    elif case == "line-neg":
        t = sub_first(t, CII_RATE0, "<ram:RateApplicablePercent>-1.00</ram:RateApplicablePercent>", "cii line rate")
    elif case == "line-absent":
        t = sub_first(t, CII_RATE0, "", "cii line rate")
    elif case.startswith("doc-"):
        rate = {"doc-0": "0.00", "doc-7": "7.00", "doc-neg": "-1.00", "doc-absent": None}[case]
        t = sub(t, "<ram:SpecifiedTradePaymentTerms>", cii_doc_block(cat, rate) + "<ram:SpecifiedTradePaymentTerms>", 1, "cii allowance/charge")
        t = sub(
            t,
            "<ram:LineTotalAmount>11693.87</ram:LineTotalAmount>",
            "<ram:LineTotalAmount>11693.87</ram:LineTotalAmount>\n"
            "        <ram:ChargeTotalAmount>10.00</ram:ChargeTotalAmount>\n"
            "        <ram:AllowanceTotalAmount>10.00</ram:AllowanceTotalAmount>",
            1,
            "cii totals",
        )
    return t


# ---------------------------------------------------------------- UBL

UBL_RATE0 = "<cbc:Percent>0.00</cbc:Percent>"
UBL_LINE_START = "<cac:CreditNoteLine>"


def ubl_doc_block(cat: str, rate: str | None) -> str:
    rate_xml = f"\n\t\t\t<cbc:Percent>{rate}</cbc:Percent>" if rate is not None else ""
    out = ""
    for indicator, reason in (("false", "Discount"), ("true", "Freight")):
        out += (
            "<cac:AllowanceCharge>\n"
            f"\t\t<cbc:ChargeIndicator>{indicator}</cbc:ChargeIndicator>\n"
            f"\t\t<cbc:AllowanceChargeReason>{reason}</cbc:AllowanceChargeReason>\n"
            '\t\t<cbc:Amount currencyID="EUR">10.00</cbc:Amount>\n'
            "\t\t<cac:TaxCategory>\n"
            f"\t\t\t<cbc:ID>{cat}</cbc:ID>{rate_xml}\n"
            "\t\t\t<cac:TaxScheme>\n\t\t\t\t<cbc:ID>VAT</cbc:ID>\n\t\t\t</cac:TaxScheme>\n"
            "\t\t</cac:TaxCategory>\n"
            "\t</cac:AllowanceCharge>\n\t"
        )
    return out


def ubl_line_edit(text: str, new_rate_xml: str) -> str:
    head, sep, line = text.partition(UBL_LINE_START)
    if not sep:
        raise SystemExit("ubl: no credit note line")
    line = sub(line, UBL_RATE0, new_rate_xml, 1, "ubl line rate")
    return head + sep + line


def ubl_probe(base: str, cat: str, case: str) -> str:
    t = sub(base, "<cbc:ID>E</cbc:ID>", f"<cbc:ID>{cat}</cbc:ID>", 2, "ubl category")
    t = sub(t, "\t\t\t\t<cbc:TaxExemptionReason>Taxes are not applicable</cbc:TaxExemptionReason>\n", "", 1, "ubl exemption reason")
    if case == "line-7":
        t = sub(t, UBL_RATE0, "<cbc:Percent>7.00</cbc:Percent>", 2, "ubl rates")
        t = sub(t, '<cbc:TaxAmount currencyID="EUR">0.00</cbc:TaxAmount>', '<cbc:TaxAmount currencyID="EUR">7.01</cbc:TaxAmount>', 2, "ubl vat")
        t = sub(t, '<cbc:TaxInclusiveAmount currencyID="EUR">100.11</cbc:TaxInclusiveAmount>', '<cbc:TaxInclusiveAmount currencyID="EUR">107.12</cbc:TaxInclusiveAmount>', 1, "ubl incl")
        t = sub(t, '<cbc:PayableAmount currencyID="EUR">100.11</cbc:PayableAmount>', '<cbc:PayableAmount currencyID="EUR">107.12</cbc:PayableAmount>', 1, "ubl payable")
    elif case == "line-neg":
        t = ubl_line_edit(t, "<cbc:Percent>-1.00</cbc:Percent>")
    elif case == "line-absent":
        t = ubl_line_edit(t, "")
    elif case.startswith("doc-"):
        rate = {"doc-0": "0.00", "doc-7": "7.00", "doc-neg": "-1.00", "doc-absent": None}[case]
        t = sub(t, "<cac:TaxTotal>", ubl_doc_block(cat, rate) + "<cac:TaxTotal>", 1, "ubl allowance/charge")
        t = sub(
            t,
            '<cbc:TaxInclusiveAmount currencyID="EUR">100.11</cbc:TaxInclusiveAmount>',
            '<cbc:TaxInclusiveAmount currencyID="EUR">100.11</cbc:TaxInclusiveAmount>\n'
            '\t\t<cbc:AllowanceTotalAmount currencyID="EUR">10.00</cbc:AllowanceTotalAmount>\n'
            '\t\t<cbc:ChargeTotalAmount currencyID="EUR">10.00</cbc:ChargeTotalAmount>',
            1,
            "ubl totals",
        )
    return t


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    cii_base = (root / "fixtures/CII_business_example_Z.xml").read_text(encoding="utf-8")
    ubl_base = (root / "fixtures/ubl-tc434-creditnote1.xml").read_text(encoding="utf-8")
    if not cii_base or not ubl_base:
        raise SystemExit("empty fixture")
    out = root / "variants/533/probes"
    n = 0
    for cat in CATEGORIES:
        for case in CASES:
            for syntax, make, base in (("cii", cii_probe, cii_base), ("ubl", ubl_probe, ubl_base)):
                dest = out / syntax / f"{cat}-{case}.xml"
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(make(base, cat, case), encoding="utf-8")
                n += 1
    print(f"wrote {n} probes under {out.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
