#!/usr/bin/env python3
"""Replay every probe in inputs/ under France_RFE v1.4.0.03 and v1.4.0.04 and print the verdict table.

Usage (from brfr/): python3 probes-v1.4.0.04/replay.py [--write]   (--write refreshes results.json)
A dynamic XPath/XSLT error makes the transformation stop: no SVRL exists, the row says ERROR, never pass.
"""
import json
import re
import sys
from pathlib import Path

from saxonche import PySaxonProcessor

PACK = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
XSLT = {
    "cii": "cii-flux2/BR-FR-Flux2-Schematron-CII.xslt",
    "ubl": "ubl-flux2/BR-FR-Flux2-Schematron-UBL.xslt",
}
ID_RE = re.compile(r'<svrl:failed-assert\b[^>]*?\bid="([^"]+)"')


def verdict(proc, tag: str, syntax: str, xml: Path) -> str:
    xslt = PACK / "vendor" / f"v1.4.0.{tag}" / XSLT[syntax]
    xp = proc.new_xslt30_processor()
    try:
        out = xp.compile_stylesheet(stylesheet_file=str(xslt)).transform_to_string(source_file=str(xml))
    except Exception as exc:  # saxonche raises on dynamic errors
        return "EXC " + str(exc).strip().split("\n")[0][:110]
    if out is None:
        return "EXC " + (xp.error_message or "").strip().split("\n")[0][:110]
    ids = ID_RE.findall(out)
    return ("fail " + ",".join(ids)) if ids else "pass"


def main() -> int:
    rows = {}
    with PySaxonProcessor(license=False) as proc:
        for xml in sorted((HERE / "inputs").glob("*.xml")):
            syntax = "cii" if xml.name.startswith("cii") else "ubl"
            row = {tag: verdict(proc, tag, syntax, xml) for tag in ("03", "04")}
            rows[xml.name] = row
            print(f"{xml.name:58s} .03: {row['03']:40.40s} .04: {row['04']}")
    if "--write" in sys.argv:
        (HERE / "results.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
