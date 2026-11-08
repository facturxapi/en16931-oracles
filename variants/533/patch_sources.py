#!/usr/bin/env python3
"""Apply the issue 533 variants to a checkout of ConnectingEurope/eInvoicing-EN16931
at tag validation-1.3.17 (commit d0dea7300c2ad60d50af4a4f31e122fdbf7c0ed3).

  V1 = two-way rename BR-IP-nn <-> BR-IG-nn in the CII binding and the CII abstract
       model (assert ids, $BR-... references, message prefixes, param names),
       done through unique temporary names, plus current BR-IP-06 / BR-IP-07
       (IGIC document-level allowance / charge rate) changed from > 0 to >= 0.
  V2 = V1 + current BR-IP-05 (IGIC line rate) changed from > 0 to >= 0, with its
       message aligned on the UBL wording of the same IGIC rule.

Only the two CII model files are touched. UBL is not modified.
Usage: patch_sources.py <upstream-checkout> V1|V2
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BINDING = "cii/schematron/CII/EN16931-CII-model.sch"
ABSTRACT = "cii/schematron/abstract/EN16931-CII-model.sch"

GT0 = 'value="ram:RateApplicablePercent &gt; 0"/>'
GE0 = 'value="ram:RateApplicablePercent &gt;= 0"/>'

# Current CII text of the IGIC line rule (named BR-IP-05 in 1.3.17).
CII_IGIC_LINE_MSG = (
    '[BR-IP-05]-In an Invoice line (BG-25) where the Invoiced item VAT category code '
    '(BT-151) is "IGIC" the invoiced item VAT rate (BT-152) shall be greater than 0 (zero).'
)
# UBL 1.3.17 text of the same IGIC rule (ubl/schematron/abstract/EN16931-model.sch, BR-IG-05),
# kept under the current CII id so that the rename step moves it to BR-IG-05.
UBL_IGIC_LINE_MSG = (
    '[BR-IP-05]-In an Invoice line (BG-25) where the Invoiced item VAT category code '
    '(BT-151) is "IGIC" the invoiced item VAT rate (BT-152) shall be 0 (zero) or greater than zero.'
)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 occurrence, found {count}")
    return text.replace(old, new)


def set_param_ge0(text: str, name: str) -> str:
    return replace_once(text, f'<param name="{name}" {GT0}', f'<param name="{name}" {GE0}', name)


def two_way_rename(text: str, label: str) -> str:
    ids = re.compile(r"BR-(IP|IG)-(\d\d)")
    before = sorted(m.group(0) for m in ids.finditer(text))
    if "__TMP533_" in text:
        raise SystemExit(f"{label}: temporary marker already present")
    text = re.sub(r"BR-IP-(\d\d)", r"__TMP533_IP_\1__", text)
    text = re.sub(r"BR-IG-(\d\d)", r"__TMP533_IG_\1__", text)
    text = re.sub(r"__TMP533_IP_(\d\d)__", r"BR-IG-\1", text)
    text = re.sub(r"__TMP533_IG_(\d\d)__", r"BR-IP-\1", text)
    if "__TMP533_" in text:
        raise SystemExit(f"{label}: temporary marker left behind")
    swapped = sorted(
        ("BR-IG-" if m.startswith("BR-IP-") else "BR-IP-") + m[-2:] for m in before
    )
    after = sorted(m.group(0) for m in ids.finditer(text))
    if after != swapped:
        raise SystemExit(f"{label}: rename is not a clean swap")
    return text


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[2] not in ("V1", "V2"):
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    variant = sys.argv[2]
    binding_path = root / BINDING
    abstract_path = root / ABSTRACT
    binding = binding_path.read_text(encoding="utf-8")
    abstract = abstract_path.read_text(encoding="utf-8")
    if not binding or not abstract:
        raise SystemExit("empty source file")

    binding = set_param_ge0(binding, "BR-IP-06")
    binding = set_param_ge0(binding, "BR-IP-07")
    if variant == "V2":
        binding = set_param_ge0(binding, "BR-IP-05")
        abstract = replace_once(abstract, CII_IGIC_LINE_MSG, UBL_IGIC_LINE_MSG, "BR-IP-05 message")

    binding = two_way_rename(binding, BINDING)
    abstract = two_way_rename(abstract, ABSTRACT)

    binding_path.write_text(binding, encoding="utf-8")
    abstract_path.write_text(abstract, encoding="utf-8")
    print(f"{variant}: patched {BINDING} and {ABSTRACT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
