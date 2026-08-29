#!/usr/bin/env python3
"""BR-CL-08 / BT-21 BAT polarity gate.

CII parent AAI and CII BAT must stay 0-fail; UBL #AAI# wrap 0-fail;
UBL #BAT# wrap must be exactly 1 failed-assert whose id is BR-CL-08.

Parses committed SVRL (gaps/receipts/*.svrl.xml and the parent
oracles/receipts/CII_example5.svrl.xml). Not a file-presence check.
Exits non-zero if CII BAT starts failing, UBL BAT becomes 0-fail,
or UBL BAT fails a different id.

Runnable outside GitHub Actions. Set ORACLE_ROOT to the checkout root.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

FAILED_RE = re.compile(r"<svrl:failed-assert\b")
FAILED_OPEN_RE = re.compile(r"<svrl:failed-assert\b([^>]*)>", re.DOTALL)
ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')
FLAG_ATTR_RE = re.compile(r'\bflag="([^"]+)"')

PARENT_CII = "CII_example5.xml"
PARENT_CII_SHA256 = (
    "473b2f9bd47b807804db7f8729eecbdd4b404c6232aca31262897bd5371d802b"
)
CII_BAT = "CII_example5-bt21-subject-BAT.xml"
CII_BAT_SHA256 = (
    "97587d713955175e6016d7800acea0a7c7253abb32417f1ac37f532568ad7de2"
)
UBL_AAI = "ubl-tc434-example5-bt21-note-AAI-wrap.xml"
UBL_AAI_SHA256 = (
    "66141952729ddf5bfa4b5916f7982196750d2f933febc083ac354d96784a4a6e"
)
UBL_BAT = "ubl-tc434-example5-bt21-note-BAT-wrap.xml"
UBL_BAT_SHA256 = (
    "12d77bf554a18b13c0407735aba4b5ae3d6ea25ef33c3cf1d5cfdbb415e079fe"
)
BRCL08 = "BR-CL-08"
EXIT_OK = 0
EXIT_DIVERGE = 1
EXIT_CONFIG = 2


def oracle_root() -> Path:
    raw = os.environ.get("ORACLE_ROOT")
    if raw:
        return Path(raw)
    return Path(__file__).resolve().parent.parent


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_svrl(path: Path) -> tuple[int, list[str], list[str]]:
    if not path.is_file():
        raise FileNotFoundError(f"missing SVRL {path}")
    text = path.read_text(encoding="utf-8")
    n_fail = len(FAILED_RE.findall(text))
    ids: list[str] = []
    flags: list[str] = []
    for m in FAILED_OPEN_RE.finditer(text):
        attrs = m.group(1)
        im = ID_ATTR_RE.search(attrs)
        ids.append(im.group(1) if im else "?")
        fm = FLAG_ATTR_RE.search(attrs)
        flags.append(fm.group(1) if fm else "")
    return n_fail, ids, flags


def check_sha(path: Path, expected: str, label: str) -> list[str]:
    if not path.is_file():
        return [f"missing {label}"]
    got = sha256_file(path)
    if got != expected:
        return [f"{label} sha {got} != expected {expected}"]
    return []


def write_summary(lines: list[str]) -> None:
    text = "\n".join(lines) + "\n"
    print(text, end="")
    dest = os.environ.get("GITHUB_STEP_SUMMARY")
    if dest:
        with open(dest, "a", encoding="utf-8") as handle:
            handle.write(text)


def main() -> int:
    root = oracle_root()
    errors: list[str] = []

    parent_xml = root / "fixtures" / PARENT_CII
    parent_svrl = root / "oracles" / "receipts" / "CII_example5.svrl.xml"
    errors.extend(check_sha(parent_xml, PARENT_CII_SHA256, f"fixtures/{PARENT_CII}"))
    try:
        n_fail, ids, _flags = parse_svrl(parent_svrl)
    except FileNotFoundError as exc:
        errors.append(str(exc))
        n_fail, ids = -1, []
    if n_fail != 0:
        errors.append(
            f"parent CII AAI fixtures/{PARENT_CII} failed_assert={n_fail} ids={ids} (expected 0)"
        )

    parent_results = root / "oracles" / "receipts" / "RESULTS.json"
    if not parent_results.is_file():
        errors.append("missing oracles/receipts/RESULTS.json")
    else:
        rows = json.loads(parent_results.read_text(encoding="utf-8"))
        parent_row = next((r for r in rows if r.get("file") == PARENT_CII), None)
        if parent_row is None:
            errors.append(f"oracles/receipts/RESULTS.json has no row for {PARENT_CII}")
        else:
            if int(parent_row.get("failed_assert", -1)) != 0:
                errors.append(
                    f"oracles RESULTS {PARENT_CII} failed_assert="
                    f"{parent_row.get('failed_assert')} (expected 0)"
                )
            if parent_row.get("sha256") != PARENT_CII_SHA256:
                errors.append(
                    f"oracles RESULTS {PARENT_CII} sha {parent_row.get('sha256')} "
                    f"!= {PARENT_CII_SHA256}"
                )

    gaps = root / "gaps"
    receipts = gaps / "receipts"
    probes = (
        (CII_BAT, CII_BAT_SHA256, 0, None, None),
        (UBL_AAI, UBL_AAI_SHA256, 0, None, None),
        (UBL_BAT, UBL_BAT_SHA256, 1, (BRCL08,), "fatal"),
    )
    for name, digest, expect_fail, expect_ids, expect_flag in probes:
        errors.extend(check_sha(gaps / name, digest, f"gaps/{name}"))
        svrl = receipts / (Path(name).stem + ".svrl.xml")
        try:
            n_fail, ids, flags = parse_svrl(svrl)
        except FileNotFoundError as exc:
            errors.append(str(exc))
            continue
        if n_fail != expect_fail:
            errors.append(
                f"{name} SVRL failed_assert={n_fail} ids={ids} (expected {expect_fail})"
            )
            continue
        if expect_ids is not None:
            if tuple(ids) != expect_ids:
                errors.append(
                    f"{name} SVRL failed-assert ids={ids} (expected {list(expect_ids)})"
                )
            if expect_flag and (not flags or flags[0] != expect_flag):
                errors.append(
                    f"{name} SVRL failed-assert flag={flags} (expected {expect_flag})"
                )

    if errors:
        write_summary(["## BR-CL-08 / BT-21 BAT polarity — DIVERGED", ""] + [f"- {e}" for e in errors])
        return EXIT_DIVERGE

    write_summary(
        [
            "## BR-CL-08 / BT-21 BAT polarity — OK",
            "",
            f"- parent AAI fixtures/{PARENT_CII} SHA `{PARENT_CII_SHA256}` failed_assert=0",
            f"- gaps/{CII_BAT} failed_assert=0 (CII BAT accepted)",
            f"- gaps/{UBL_AAI} failed_assert=0 (UBL #AAI# wrap accepted)",
            f"- gaps/{UBL_BAT} failed_assert=1 id={BRCL08} fatal (UBL #BAT# wrap rejected)",
        ]
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
