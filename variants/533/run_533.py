#!/usr/bin/env python3
"""Run the issue 533 probes and checks with SaxonC-HE 13.0 and write RESULTS.json / RESULTS.md.

CII stylesheets: PUBLISHED (vendor/en16931-1.3.17, release zip), BASE (rebuilt from the tag,
unpatched), V1 and V2 (variants/533/xslt, see build.sh). UBL: the published release XSLT,
unchanged in every variant.

Checks:
  static   for each BR-IG-nn / BR-IP-nn assertion of each stylesheet, the regime its message
           names (IGIC / IPSI); CII must match UBL id by id.
  probes   32 probes (make_probes.py): failed-assert ids per stylesheet; within the
           BR-IG / BR-IP families, CII must give the same ids as UBL for the same mutation.
  nonreg   every extra CII document (fixtures/*.xml CII, plus --examples / --vefa dirs):
           V1 and V2 must give the same (id, location) list as PUBLISHED.

Usage: run_533.py [--root .] [--examples DIR] [--vefa DIR] [--write | --check]
--check replays and compares with the committed RESULTS.json (probe and fixture part only).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from saxonche import PySaxonProcessor

SVRL = "{http://purl.oclc.org/dsdl/svrl}"
VEFA = "{http://difi.no/xsd/vefa/validator/1.0}"
FAMILY = re.compile(r"^BR-I[GP]-\d\d$")
VARIANTS = ("PUBLISHED", "BASE", "V1", "V2")
CATEGORIES = ("L", "M")
CASES = ("line-0", "line-7", "line-neg", "line-absent", "doc-0", "doc-7", "doc-neg", "doc-absent")
REGIME = {"L": "IGIC", "M": "IPSI"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stylesheets(root: Path) -> dict[str, Path]:
    v = root / "variants/533/xslt"
    return {
        "PUBLISHED": root / "vendor/en16931-1.3.17/xslt/EN16931-CII-validation.xslt",
        "BASE": v / "BASE/EN16931-CII-validation.xslt",
        "V1": v / "V1/EN16931-CII-validation.xslt",
        "V2": v / "V2/EN16931-CII-validation.xslt",
        "UBL": root / "vendor/en16931-1.3.17/xslt/EN16931-UBL-validation.xslt",
    }


def static_regimes(xslt: Path) -> dict[str, str]:
    """BR-IG / BR-IP id -> regime named by its message, read from the compiled XSLT."""
    text = xslt.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for m in re.finditer(r'<xsl:attribute name="id">(BR-I[GP]-\d\d)</xsl:attribute>.*?<svrl:text>(.*?)</svrl:text>', text, re.S):
        rid, msg = m.group(1), m.group(2)
        regimes = sorted(set(re.findall(r"IGIC|IPSI", msg)))
        out[rid] = "/".join(regimes) or "?"
    return dict(sorted(out.items()))


class Runner:
    def __init__(self, proc: PySaxonProcessor, sheets: dict[str, Path]):
        self.proc = proc
        xp = proc.new_xslt30_processor()
        self.compiled = {k: xp.compile_stylesheet(stylesheet_file=str(p)) for k, p in sheets.items()}

    def run(self, sheet: str, *, path: Path | None = None, text: str | None = None) -> list[list[str]]:
        exe = self.compiled[sheet]
        if path is not None:
            svrl = exe.transform_to_string(source_file=str(path))
        else:
            node = self.proc.parse_xml(xml_text=text)
            svrl = exe.transform_to_string(xdm_node=node)
        tree = ET.fromstring(svrl)
        return sorted([fa.get("id") or "", fa.get("location") or ""] for fa in tree.iter(SVRL + "failed-assert"))


def ids(fails: list[list[str]]) -> list[str]:
    return sorted({f[0] for f in fails})


def family(id_list: list[str]) -> list[str]:
    return [i for i in id_list if FAMILY.match(i)]


def rate_rule(case: str, cat: str, syntax_ids: list[str]) -> str:
    """Which rate rule fired: -05 for line cases, -06/-07 for document cases."""
    nums = ("05",) if case.startswith("line") else ("06", "07")
    hit = [i for i in syntax_ids if FAMILY.match(i) and i[-2:] in nums]
    return ", ".join(hit) if hit else "none"


def vefa_documents(vefa_dir: Path) -> list[tuple[str, str, list[tuple[str, str]]]]:
    """(name, document xml, [(success|error, id)]) for each <test> of each testSet."""
    out = []
    for f in sorted(vefa_dir.glob("*.xml")):
        tree = ET.parse(f)
        for n, test in enumerate(tree.getroot().iter(VEFA + "test"), 1):
            expect: list[tuple[str, str]] = []
            doc = None
            for child in test:
                if child.tag == VEFA + "assert":
                    for e in child:
                        tag = e.tag.replace(VEFA, "")
                        if tag in ("success", "error", "warning"):
                            expect.append((tag, (e.text or "").strip()))
                else:
                    doc = child
            if doc is not None:
                out.append((f"{f.name}#{n}", ET.tostring(doc, encoding="unicode"), expect))
    return out


def other_rules_line(r: dict) -> str:
    others = sorted({i for p in r["probes"] for k in ("UBL",) + VARIANTS for i in p[k] if not FAMILY.match(i)})
    if not others:
        return "No rule outside BR-IG / BR-IP fired on any probe, in any stylesheet."
    return "Rules outside BR-IG / BR-IP also fired (see RESULTS.json): " + ", ".join(f"`{i}`" for i in others) + "."


def render_md(r: dict) -> str:
    def cell(id_list: list[str]) -> str:
        fam = family(id_list)
        return ", ".join(f"`{i}`" for i in fam) if fam else "—"

    lines = [
        "# Issue 533 — V1 / V2 results",
        "",
        "Generated by `variants/533/run_533.py --write` (do not edit by hand).",
        f"Engine: {r['engine']}. Upstream: `{r['upstream']['tag']}` = `{r['upstream']['commit']}`.",
        "",
        "| Stylesheet | SHA-256 |",
        "|---|---|",
    ]
    for k, v in r["xslt_sha256"].items():
        lines.append(f"| {k} | `{v}` |")
    for k, v in r["patch_sha256"].items():
        lines.append(f"| patch {k} | `{v}` |")
    lines += [
        "",
        "## Probes: BR-IG / BR-IP failed-asserts",
        "",
        other_rules_line(r),
        "UBL = published 1.3.17 UBL XSLT (unchanged in every variant).",
        "",
        "| Probe | UBL | CII published | CII V1 | CII V2 | V1 = UBL | V2 = UBL |",
        "|---|---|---|---|---|---|---|",
    ]
    for p in r["probes"]:
        def same(v: str) -> str:
            d = p["family_diff_vs_ubl"][v]
            return "yes" if not d else "no (" + ", ".join(f"`{i}`" for i in d) + ")"
        lines.append(
            f"| `{p['probe']}` | {cell(p['UBL'])} | {cell(p['PUBLISHED'])} | {cell(p['V1'])} | {cell(p['V2'])} | {same('V1')} | {same('V2')} |"
        )
    lines += [
        "",
        "`BASE` (tag rebuilt without patch) gives the same ids as `published` on every probe: "
        + ("yes." if all(p["BASE"] == p["PUBLISHED"] for p in r["probes"]) else "**no**."),
        "",
        "## Static: regime named by each BR-IG / BR-IP message",
        "",
        "| Stylesheet | ids whose regime differs from UBL |",
        "|---|---|",
    ]
    for v, bad in r["static_mismatch"].items():
        lines.append(f"| {v} | {len(bad)} of 20{(': ' + ', '.join(bad)) if bad and len(bad) < 20 else ''} |")
    lines += [
        "",
        "## Non-regression (V1 / V2 vs published, same (id, location) list)",
        "",
        "| Document | failed-asserts (published) | V1 same | V2 same | VEFA expectations met (pub / V1 / V2) |",
        "|---|---|---|---|---|",
    ]
    for e in r["nonreg"]:
        vefa = e.get("vefa_expectations_met")
        vefa_cell = " / ".join("yes" if vefa[k] else "no" for k in ("PUBLISHED", "V1", "V2")) if vefa else ""
        lines.append(
            f"| `{e['doc']}` | {e['failed_asserts']} | {'yes' if e['same_as_published']['V1'] else 'no'} | "
            f"{'yes' if e['same_as_published']['V2'] else 'no'} | {vefa_cell} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--examples", help="extra dir of CII documents (e.g. upstream cii/examples)")
    ap.add_argument("--vefa", help="upstream test/cii dir (VEFA testSets)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    base = root / "variants/533"
    sheets = stylesheets(root)
    pinned = {}
    for line in (base / "xslt/SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split()
        pinned[name.split("/")[0]] = digest
    for k in ("BASE", "V1", "V2"):
        if sha256(sheets[k]) != pinned[k]:
            raise SystemExit(f"{k}: XSLT does not match variants/533/xslt/SHA256SUMS")

    result: dict = {
        "engine": "SaxonC-HE 13.0 (saxonche 13.0.0)",
        "upstream": {"tag": "validation-1.3.17", "commit": "d0dea7300c2ad60d50af4a4f31e122fdbf7c0ed3"},
        "xslt_sha256": {k: sha256(p) for k, p in sheets.items()},
        "patch_sha256": {v: sha256(base / f"patches/{v}.patch") for v in ("V1", "V2")},
    }
    mismatches: list[str] = []

    # static
    ubl_static = static_regimes(sheets["UBL"])
    result["static"] = {"UBL": ubl_static}
    for v in VARIANTS:
        st = static_regimes(sheets[v])
        result["static"][v] = st
        bad = [i for i in sorted(set(st) | set(ubl_static)) if st.get(i) != ubl_static.get(i)]
        result.setdefault("static_mismatch", {})[v] = bad
    for rid, reg in ubl_static.items():
        want = "IGIC" if rid.startswith("BR-IG") else "IPSI"
        if reg != want:
            mismatches.append(f"UBL static: {rid} names {reg}")

    with PySaxonProcessor(license=False) as proc:
        runner = Runner(proc, sheets)
        # probes
        probes = []
        for cat in CATEGORIES:
            for case in CASES:
                cii = base / f"probes/cii/{cat}-{case}.xml"
                ubl = base / f"probes/ubl/{cat}-{case}.xml"
                row = {
                    "probe": f"{cat}-{case}",
                    "cii_sha256": sha256(cii),
                    "ubl_sha256": sha256(ubl),
                    "UBL": ids(runner.run("UBL", path=ubl)),
                }
                for v in VARIANTS:
                    row[v] = ids(runner.run(v, path=cii))
                row["family_match"] = {v: family(row[v]) == family(row["UBL"]) for v in VARIANTS}
                row["family_diff_vs_ubl"] = {
                    v: sorted(set(family(row[v])) ^ set(family(row["UBL"]))) for v in VARIANTS
                }
                row["rate_rule"] = {k: rate_rule(case, cat, row[k]) for k in ("UBL",) + VARIANTS}
                probes.append(row)
        result["probes"] = probes

        # non-regression
        docs: list[tuple[str, Path | None, str | None, list]] = []
        for f in sorted((root / "fixtures").glob("*.xml")):
            if "CrossIndustryInvoice" in f.read_text(encoding="utf-8")[:2000]:
                docs.append((f"fixtures/{f.name}", f, None, []))
        if args.examples:
            for f in sorted(Path(args.examples).glob("*.xml")):
                docs.append((f"examples/{f.name}", f, None, []))
        if args.vefa:
            for name, xml, expect in vefa_documents(Path(args.vefa)):
                docs.append((f"vefa/{name}", None, xml, expect))
        nonreg = []
        for name, path, text, expect in docs:
            runs = {v: runner.run(v, path=path, text=text) for v in ("PUBLISHED", "V1", "V2")}
            entry = {
                "doc": name,
                "failed_asserts": len(runs["PUBLISHED"]),
                "same_as_published": {v: runs[v] == runs["PUBLISHED"] for v in ("V1", "V2")},
            }
            if path is not None:
                entry["sha256"] = sha256(path)
            if expect:
                fired = {v: {f[0] for f in runs[v]} for v in runs}
                entry["vefa_expectations_met"] = {
                    v: all((rid in fired[v]) == (kind == "error") for kind, rid in expect if kind in ("success", "error"))
                    for v in runs
                }
            nonreg.append(entry)
        result["nonreg"] = nonreg

    for row in probes:
        for v in ("V1", "V2"):
            if not row["family_match"][v]:
                mismatches.append(f"{row['probe']}: {v} BR-IG/BR-IP ids differ from UBL")
    for entry in nonreg:
        for v in ("V1", "V2"):
            if not entry["same_as_published"][v]:
                mismatches.append(f"{entry['doc']}: {v} differs from PUBLISHED")
    result["mismatches"] = mismatches

    out_json = base / "RESULTS.json"
    if args.check:
        committed = json.loads(out_json.read_text(encoding="utf-8"))
        local_only = ("examples/", "vefa/")
        keep = lambda r: {
            **r,
            "nonreg": [e for e in r["nonreg"] if not e["doc"].startswith(local_only)],
            "mismatches": [m for m in r["mismatches"] if not m.startswith(local_only)],
        }
        if keep(committed) != keep(result):
            print("variants/533: replay differs from committed RESULTS.json", file=sys.stderr)
            return 1
        print(f"variants/533: replay matches RESULTS.json ({len(probes)} probes, {sum(1 for e in nonreg)} documents)")
        return 0
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        out_json.write_text(text, encoding="utf-8")
        (base / "RESULTS.md").write_text(render_md(result), encoding="utf-8")
    else:
        print(text)
    print(f"{len(probes)} probes, {len(nonreg)} non-regression documents, {len(mismatches)} check mismatches", file=sys.stderr)
    for e in mismatches:
        print("  " + e, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
