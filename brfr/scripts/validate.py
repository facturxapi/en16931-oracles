#!/usr/bin/env python3
"""Runner BR-FR Flux2 — XSLT officiel France_RFE, SaxonC-HE 13.0.

Ne journalise jamais les octets des factures.
N'appelle aucun validateur commercial / facturxapi.com.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SOURCE_DATE_EPOCH = "1771286400"
os.environ.setdefault("SOURCE_DATE_EPOCH", SOURCE_DATE_EPOCH)

ENGINE = "SaxonC-HE 13.0"
ENGINE_PKG = "saxonche 13.0.0"
RECEIPT_DATE = "16 Aug 2026 PT"

PACK = Path(__file__).resolve().parent.parent

XSLT = {
    ("02", "ubl"): PACK / "vendor/v1.4.0.02/ubl-flux2/BR-FR-Flux2-Schematron-UBL.xslt",
    ("03", "ubl"): PACK / "vendor/v1.4.0.03/ubl-flux2/BR-FR-Flux2-Schematron-UBL.xslt",
    ("02", "cii"): PACK / "vendor/v1.4.0.02/cii-flux2/BR-FR-Flux2-Schematron-CII.xslt",
    ("03", "cii"): PACK / "vendor/v1.4.0.03/cii-flux2/BR-FR-Flux2-Schematron-CII.xslt",
}

EXPECTED_XSLT_SHA = {
    ("02", "ubl"): "e308eade08e21ad69881328a2c14290ec2877b02b7ec873531baf82aae2f6628",
    ("03", "ubl"): "4a54e8b363907b7ca13c6d63302910aa7e42681fdaa6d16ef18b9a414973c09c",
    ("02", "cii"): "a5509334f70a3c8268f0339a968c49185c17cba60f71c8f6fc095deba94e6438",
    ("03", "cii"): "a5509334f70a3c8268f0339a968c49185c17cba60f71c8f6fc095deba94e6438",
}

FAILED_RE = re.compile(r"<svrl:failed-assert\b")
FIRED_RE = re.compile(r"<svrl:fired-rule\b")
FAILED_OPEN_RE = re.compile(r"<svrl:failed-assert\b([^>]*)>")
ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_syntax(xml_path: Path) -> str:
    head = xml_path.read_bytes()[:4000]
    if b"CrossIndustryInvoice" in head:
        return "cii"
    return "ubl"


def failed_ids(svrl: str) -> list[str]:
    ids = []
    for m in FAILED_OPEN_RE.finditer(svrl):
        am = ID_ATTR_RE.search(m.group(1))
        ids.append(am.group(1) if am else "(sans-id)")
    return ids


def transform(xml_path: Path, xslt_path: Path) -> str:
    try:
        from saxonche import PySaxonProcessor
    except ImportError:
        print(
            "ERREUR: saxonche n'est pas installé.\n"
            "  python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(2)
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        executable = xsltproc.compile_stylesheet(stylesheet_file=str(xslt_path))
        if executable is None:
            print(f"ERREUR: compilation XSLT échouée : {xslt_path}", file=sys.stderr)
            sys.exit(2)
        svrl = executable.transform_to_string(source_file=str(xml_path))
        if svrl is None:
            print(f"ERREUR: transformation sans résultat : {xml_path.name}", file=sys.stderr)
            sys.exit(2)
        return svrl


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="fixtures", help="répertoire de XML")
    ap.add_argument("--out-dir", default="receipts/v1.4.0.03")
    ap.add_argument("--tag", choices=["02", "03"], default="03")
    ap.add_argument("files", nargs="*", help="fichiers XML (sinon *.xml du --dir)")
    args = ap.parse_args()

    xml_dir = (PACK / args.dir).resolve() if not Path(args.dir).is_absolute() else Path(args.dir)
    out_dir = (PACK / args.out_dir).resolve() if not Path(args.out_dir).is_absolute() else Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.files:
        xmls = [Path(f) if Path(f).is_absolute() else xml_dir / f for f in args.files]
    else:
        xmls = sorted(xml_dir.glob("*.xml"))
    if not xmls:
        print(f"ERREUR: aucun XML dans {xml_dir}", file=sys.stderr)
        return 2

    rows = []
    for xml_path in xmls:
        syntax = detect_syntax(xml_path)
        xslt = XSLT[(args.tag, syntax)]
        exp = EXPECTED_XSLT_SHA[(args.tag, syntax)]
        xsha = sha256_file(xslt)
        if xsha != exp:
            print(f"ERREUR: SHA256 XSLT inattendu {xslt}\n  attendu {exp}\n  obtenu  {xsha}", file=sys.stderr)
            return 2
        fsha = sha256_file(xml_path)
        svrl = transform(xml_path, xslt)
        fired = len(FIRED_RE.findall(svrl))
        failed = len(FAILED_RE.findall(svrl))
        ids = failed_ids(svrl)
        svrl_path = out_dir / f"{xml_path.stem}.svrl.xml"
        svrl_path.write_text(svrl, encoding="utf-8")
        oneline = out_dir / f"{xml_path.stem}.oneline.txt"
        oneline.write_text(
            f"{xml_path.name}\ttag=v1.4.0.{args.tag}\tsyntax={syntax}\tfailed={failed}\tids={','.join(ids)}\tsha256={fsha}\txslt={xsha}\n",
            encoding="utf-8",
        )
        receipt = out_dir / f"{xml_path.stem}.receipt.md"
        receipt.write_text(
            f"# Recette SVRL — {xml_path.name}\n\n"
            f"- Date : {RECEIPT_DATE}\n"
            f"- Artefact : France_RFE v1.4.0.{args.tag} BR-FR-Flux2 {syntax.upper()}\n"
            f"- XSLT : `{xslt.relative_to(PACK)}`\n"
            f"- SHA256 XSLT : `{xsha}`\n"
            f"- SHA256 fixture : `{fsha}`\n"
            f"- Moteur : {ENGINE} ({ENGINE_PKG})\n"
            f"- `svrl:fired-rule` : {fired}\n"
            f"- `svrl:failed-assert` : {failed}\n"
            f"- ids : {', '.join(ids) if ids else '(aucun)'}\n"
            f"- SOURCE_DATE_EPOCH : {SOURCE_DATE_EPOCH}\n",
            encoding="utf-8",
        )
        rows.append(
            {
                "file": xml_path.name,
                "syntax": syntax,
                "tag": f"v1.4.0.{args.tag}",
                "failed_assert": failed,
                "fired_rule": fired,
                "ids": ids,
                "sha256": fsha,
                "xslt_sha256": xsha,
            }
        )
        print(f"{xml_path.name}\t{syntax}\tv1.4.0.{args.tag}\tfailed={failed}\tids={','.join(ids) or '-'}")

    results = out_dir / "RESULTS.json"
    payload = {"engine": ENGINE, "tag": f"v1.4.0.{args.tag}", "date": RECEIPT_DATE, "results": rows}
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    results.write_text(text, encoding="utf-8")
    (out_dir / "RESULTS.sha256").write_text(hashlib.sha256(text.encode()).hexdigest() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
