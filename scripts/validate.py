#!/usr/bin/env python3
"""Reproducteur EN16931 1.3.16 — XSLT officiel, SaxonC-HE 13.0.

Bi-mode :
  --mode reference (défaut)
      XSLT vendored : vendor/en16931-1.3.16/xslt/
      Verdict normatif.
  --mode cross-platform
      Mêmes octets XSLT. Si vendor/ est absent, télécharge les deux ZIP
      officiels, vérifie leur SHA256 (épinglés), n'extrait que les deux
      XSLT, puis valide. Échec non-zéro si le téléchargement est impossible
      (pas de saut silencieux).

Ne journalise jamais les octets des factures.
N'appelle aucun validateur commercial.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
import shutil
import tempfile
import zipfile
from pathlib import Path

SOURCE_DATE_EPOCH = "1771286400"
os.environ.setdefault("SOURCE_DATE_EPOCH", SOURCE_DATE_EPOCH)

ENGINE = "SaxonC-HE 13.0"
ENGINE_PKG = "saxonche 13.0.0"
RECEIPT_DATE = "16 Aug 2026 PT"
PHRASE = "machine-verified candidate — EN16931 1.3.16 official XSLT"

CII_ZIP_URL = (
    "https://github.com/ConnectingEurope/eInvoicing-EN16931/"
    "releases/download/validation-1.3.16/en16931-cii-1.3.16.zip"
)
UBL_ZIP_URL = (
    "https://github.com/ConnectingEurope/eInvoicing-EN16931/"
    "releases/download/validation-1.3.16/en16931-ubl-1.3.16.zip"
)
CII_ZIP_SHA256 = "1cd53cb8a84d38aedc82c0caede217da983a7934dd663f793a092fd66443c561"
UBL_ZIP_SHA256 = "bafada015efbc5248bf5e05ad2191e1d9833ef96e9dd5f4bce420a747342da85"

CII_XSLT_NAME = "EN16931-CII-validation.xslt"
UBL_XSLT_NAME = "EN16931-UBL-validation.xslt"
CII_XSLT_ZIP_PATH = "xslt/EN16931-CII-validation.xslt"
UBL_XSLT_ZIP_PATH = "xslt/EN16931-UBL-validation.xslt"
CII_XSLT_SHA256 = "0b234dea2bbfee739b7761e607a992c17fab88773014ef56355b6158cfb1cc53"
UBL_XSLT_SHA256 = "39f9d282867f1a49e7708d9e29a53da89643e1ee56f10cec1ebcf1277595fcbd"

LOGICAL_CII_XSLT = "vendor/en16931-1.3.16/xslt/EN16931-CII-validation.xslt"
LOGICAL_UBL_XSLT = "vendor/en16931-1.3.16/xslt/EN16931-UBL-validation.xslt"

USER_AGENT = "en16931-repo-v1-validate/1.0 (+reproducible CEN 1.3.16 runner)"

FIRED_RE = re.compile(r"<svrl:fired-rule\b")
FAILED_RE = re.compile(r"<svrl:failed-assert\b")
FAILED_OPEN_RE = re.compile(r"<svrl:failed-assert\b([^>]*)>")
ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')
EXPECTED_RESULTS_SHA256 = (
    "dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def load_sha256sums(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        digest, name = line.split(None, 1)
        out[name] = digest
    return out


def check_fixtures(repo: Path) -> dict[str, str]:
    sums_path = repo / "fixtures" / "SHA256SUMS"
    if not sums_path.is_file():
        print("ERREUR: fixtures/SHA256SUMS introuvable.", file=sys.stderr)
        sys.exit(2)
    expected = load_sha256sums(sums_path)
    if not expected:
        print("ERREUR: fixtures/SHA256SUMS vide.", file=sys.stderr)
        sys.exit(2)
    errors = []
    got: dict[str, str] = {}
    for name, digest in expected.items():
        fpath = repo / "fixtures" / name
        if not fpath.is_file():
            errors.append(f"manquant: {name}")
            continue
        actual = sha256_file(fpath)
        got[name] = actual
        if actual != digest:
            errors.append(f"SHA256 mismatch {name}: attendu {digest}, obtenu {actual}")
    if errors:
        print("ERREUR: contrôle d'intégrité des fixtures échoué.", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(2)
    return got


def failed_assert_ids(svrl: str) -> list[str]:
    ids: list[str] = []
    for m in FAILED_OPEN_RE.finditer(svrl):
        im = ID_ATTR_RE.search(m.group(1))
        ids.append(im.group(1) if im else "?")
    return ids


def collect_xml(xml_dir: Path) -> dict[str, str]:
    files = sorted(
        p.name
        for p in xml_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".xml"
    )
    if not files:
        print(f"ERREUR: aucun XML dans {xml_dir}", file=sys.stderr)
        sys.exit(2)
    return {name: sha256_file(xml_dir / name) for name in files}


def resolve_user_path(repo: Path, raw: str | None, default: Path) -> Path:
    if raw is None:
        return default
    path = Path(raw)
    if path.is_absolute():
        return path
    cwd_c = Path.cwd() / path
    if cwd_c.exists():
        return cwd_c.resolve()
    return (repo / path).resolve()


def source_label(repo: Path, xml_dir: Path, filename: str) -> str:
    full = (xml_dir / filename).resolve()
    try:
        return str(full.relative_to(repo.resolve()))
    except ValueError:
        return f"{xml_dir.name}/{filename}"


def syntax_of(filename: str) -> str:
    return "UBL" if filename.lower().startswith("ubl-") else "CII"


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(
            "ERREUR: téléchargement impossible (mode cross-platform, pas de saut).\n"
            f"  URL : {url}\n"
            f"  Cause : {exc}\n"
            "  Placez vendor/en16931-1.3.16/xslt/ ou réessayez le réseau.",
            file=sys.stderr,
        )
        sys.exit(2)
    dest.write_bytes(data)


def extract_xslt_from_zip(zip_path: Path, inner: str, dest: Path, expected_sha: str) -> None:
    try:
        with zipfile.ZipFile(zip_path) as zf:
            data = zf.read(inner)
    except (KeyError, zipfile.BadZipFile, OSError) as exc:
        print(
            f"ERREUR: extraction XSLT impossible depuis {zip_path.name} ({inner}): {exc}",
            file=sys.stderr,
        )
        sys.exit(2)
    digest = sha256_bytes(data)
    if digest != expected_sha:
        print(
            f"ERREUR: SHA256 XSLT extrait ({inner}) ne correspond pas.\n"
            f"  attendu {expected_sha}\n"
            f"  obtenu  {digest}",
            file=sys.stderr,
        )
        sys.exit(2)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def resolve_xslt(repo: Path, mode: str) -> tuple[Path, Path]:
    vendor_cii = repo / "vendor" / "en16931-1.3.16" / "xslt" / CII_XSLT_NAME
    vendor_ubl = repo / "vendor" / "en16931-1.3.16" / "xslt" / UBL_XSLT_NAME

    if mode == "reference":
        if not vendor_cii.is_file() or not vendor_ubl.is_file():
            print(
                "ERREUR: mode reference — XSLT vendored manquant.\n"
                "  Attendu : vendor/en16931-1.3.16/xslt/EN16931-CII-validation.xslt\n"
                "            vendor/en16931-1.3.16/xslt/EN16931-UBL-validation.xslt\n"
                "  Relancez avec --mode cross-platform pour télécharger les ZIP officiels.",
                file=sys.stderr,
            )
            sys.exit(2)
        for path, exp in ((vendor_cii, CII_XSLT_SHA256), (vendor_ubl, UBL_XSLT_SHA256)):
            got = sha256_file(path)
            if got != exp:
                print(
                    f"ERREUR: SHA256 XSLT vendored incorrect pour {path.name}.\n"
                    f"  attendu {exp}\n  obtenu  {got}",
                    file=sys.stderr,
                )
                sys.exit(2)
        return vendor_cii, vendor_ubl

    # cross-platform: use vendor if present and matching, else download
    if vendor_cii.is_file() and vendor_ubl.is_file():
        cii_ok = sha256_file(vendor_cii) == CII_XSLT_SHA256
        ubl_ok = sha256_file(vendor_ubl) == UBL_XSLT_SHA256
        if cii_ok and ubl_ok:
            return vendor_cii, vendor_ubl
        print(
            "AVERTISSEMENT: vendor/ présent mais SHA256 XSLT inattendu ; "
            "téléchargement des ZIP officiels.",
            file=sys.stderr,
        )

    cache = repo / ".cache" / "en16931-1.3.16"
    cii_zip = cache / "en16931-cii-1.3.16.zip"
    ubl_zip = cache / "en16931-ubl-1.3.16.zip"

    if not (cii_zip.is_file() and sha256_file(cii_zip) == CII_ZIP_SHA256):
        print(f"Téléchargement ZIP CII 1.3.16 → {cii_zip}")
        download(CII_ZIP_URL, cii_zip)
        got = sha256_file(cii_zip)
        if got != CII_ZIP_SHA256:
            print(
                f"ERREUR: SHA256 ZIP CII incorrect.\n  attendu {CII_ZIP_SHA256}\n  obtenu  {got}",
                file=sys.stderr,
            )
            sys.exit(2)
    if not (ubl_zip.is_file() and sha256_file(ubl_zip) == UBL_ZIP_SHA256):
        print(f"Téléchargement ZIP UBL 1.3.16 → {ubl_zip}")
        download(UBL_ZIP_URL, ubl_zip)
        got = sha256_file(ubl_zip)
        if got != UBL_ZIP_SHA256:
            print(
                f"ERREUR: SHA256 ZIP UBL incorrect.\n  attendu {UBL_ZIP_SHA256}\n  obtenu  {got}",
                file=sys.stderr,
            )
            sys.exit(2)

    xslt_dir = cache / "xslt"
    cii_xslt = xslt_dir / CII_XSLT_NAME
    ubl_xslt = xslt_dir / UBL_XSLT_NAME
    extract_xslt_from_zip(cii_zip, CII_XSLT_ZIP_PATH, cii_xslt, CII_XSLT_SHA256)
    extract_xslt_from_zip(ubl_zip, UBL_XSLT_ZIP_PATH, ubl_xslt, UBL_XSLT_SHA256)
    return cii_xslt, ubl_xslt


def transform(xml_path: Path, xslt_path: Path) -> str:
    try:
        from saxonche import PySaxonProcessor
    except ImportError:
        print(
            "ERREUR: saxonche n'est pas installé.\n"
            "  python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt\n"
            "  puis : .venv/bin/python scripts/validate.py",
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
            print(f"ERREUR: transformation XSLT sans résultat : {xml_path.name}", file=sys.stderr)
            sys.exit(2)
        return svrl


def count_svrl(svrl: str) -> tuple[int, int]:
    return len(FIRED_RE.findall(svrl)), len(FAILED_RE.findall(svrl))


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"


def write_receipt(
    dest: Path,
    *,
    filename: str,
    fixture_sha: str,
    xslt_logical: str,
    xslt_sha: str,
    fired: int,
    failed: int,
    source: str | None = None,
    rule_ids: list[str] | None = None,
) -> None:
    stem = Path(filename).stem
    label = source if source is not None else f"fixtures/{filename}"
    text = (
        f"# Recette SVRL — {filename}\n"
        f"\n"
        f"**{PHRASE}**\n"
        f"\n"
        f"- Fixture : `{label}`\n"
        f"- SHA256 fixture : `{fixture_sha}`\n"
        f"- XSLT : `{xslt_logical}`\n"
        f"- SHA256 XSLT : `{xslt_sha}`\n"
        f"- Moteur : {ENGINE} ({ENGINE_PKG})\n"
        f"- Date : {RECEIPT_DATE}\n"
        f"- `svrl:fired-rule` : {fired}\n"
        f"- `svrl:failed-assert` : {failed}\n"
        f"- SOURCE_DATE_EPOCH : {SOURCE_DATE_EPOCH}\n"
    )
    if rule_ids:
        text += f"- ids : {', '.join(rule_ids)}\n"
    dest.write_text(text, encoding="utf-8")


def load_expected(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data["fixtures"] if isinstance(data, dict) and "fixtures" in data else data
    return {row["file"]: row for row in rows}


def run_validation(
    repo: Path,
    *,
    mode: str,
    xml_dir: Path,
    receipts_dir: Path,
    require_integrity: bool,
    use_expected: bool,
    allow_fired_drift: bool,
    fail_on_failed_assert: bool,
    extra_results_dir: Path | None = None,
) -> tuple[int, str]:
    receipts_dir.mkdir(parents=True, exist_ok=True)

    if require_integrity:
        fixture_hashes = check_fixtures(repo)
    else:
        if not xml_dir.is_dir():
            print(f"ERREUR: repertoire introuvable : {xml_dir}", file=sys.stderr)
            sys.exit(2)
        fixture_hashes = collect_xml(xml_dir)
    names = sorted(fixture_hashes)
    cii_xslt, ubl_xslt = resolve_xslt(repo, mode)
    cii_sha = sha256_file(cii_xslt)
    ubl_sha = sha256_file(ubl_xslt)

    results = []
    any_failed = False
    drift_items = []

    expected_path = repo / "scripts" / "expected.json"
    expected = load_expected(expected_path) if (use_expected and expected_path.is_file()) else {}

    print(f"Moteur : {ENGINE} ({ENGINE_PKG})")
    print(f"Mode   : {mode}")
    print(f"Date   : {RECEIPT_DATE}  (SOURCE_DATE_EPOCH={SOURCE_DATE_EPOCH})")
    print(f"XML    : {xml_dir}")
    print(f"Out    : {receipts_dir}")
    print()
    print(f"{'fichier':<38} {'syn':<4} {'fired':>6} {'fail':>5}  verdict  ids")
    print("-" * 88)

    for name in names:
        syntax = syntax_of(name)
        xslt_path = ubl_xslt if syntax == "UBL" else cii_xslt
        xslt_logical = LOGICAL_UBL_XSLT if syntax == "UBL" else LOGICAL_CII_XSLT
        xslt_sha = ubl_sha if syntax == "UBL" else cii_sha
        xml_path = xml_dir / name
        svrl = transform(xml_path, xslt_path)
        fired, failed = count_svrl(svrl)
        rule_ids = failed_assert_ids(svrl)
        (receipts_dir / f"{Path(name).stem}.svrl.xml").write_text(svrl, encoding="utf-8")
        write_receipt(
            receipts_dir / f"{Path(name).stem}.receipt.md",
            filename=name,
            fixture_sha=fixture_hashes[name],
            xslt_logical=xslt_logical,
            xslt_sha=xslt_sha,
            fired=fired,
            failed=failed,
            source=source_label(repo, xml_dir, name),
            rule_ids=rule_ids,
        )
        row = {
            "engine": ENGINE,
            "failed_assert": failed,
            "file": name,
            "fired_rule": fired,
            "sha256": fixture_hashes[name],
            "syntax": syntax,
            "xslt": xslt_logical,
        }
        exp = expected.get(name)
        if exp is not None and int(exp.get("fired_rule", fired)) != fired:
            row["drift"] = True
            row["fired_rule_expected"] = int(exp["fired_rule"])
            drift_items.append(name)
        results.append(row)
        if failed > 0:
            any_failed = True
        verdict = "FAIL" if failed > 0 else "0-failed-assert"
        ids_s = ",".join(rule_ids) if rule_ids else ""
        print(f"{name:<38} {syntax:<4} {fired:6d} {failed:5d}  {verdict}  {ids_s}")

    results.sort(key=lambda r: r["file"])
    # hashed object: specified fields only (no timestamps). drift flags stay
    # in a sibling report if present, but also on the item when measured.
    hashed = []
    for row in results:
        item = {
            "engine": row["engine"],
            "failed_assert": row["failed_assert"],
            "file": row["file"],
            "fired_rule": row["fired_rule"],
            "sha256": row["sha256"],
            "syntax": row["syntax"],
            "xslt": row["xslt"],
        }
        if row.get("drift"):
            item["drift"] = True
            item["fired_rule_expected"] = row["fired_rule_expected"]
        hashed.append(item)

    canonical = canonical_json(hashed)
    results_path = receipts_dir / "RESULTS.json"
    results_path.write_text(canonical, encoding="utf-8")
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    sha_line = f"{digest}  RESULTS.json\n"
    (receipts_dir / "RESULTS.sha256").write_text(sha_line, encoding="utf-8")
    if extra_results_dir is not None:
        extra_results_dir.mkdir(parents=True, exist_ok=True)
        (extra_results_dir / "RESULTS.json").write_text(canonical, encoding="utf-8")
        (extra_results_dir / "RESULTS.sha256").write_text(sha_line, encoding="utf-8")

    print("-" * 88)
    print(f"RESULTS.json  : {results_path}")
    print(f"RESULTS.sha256: {digest}")
    if drift_items:
        print(f"DRIFT fired-rule : {', '.join(drift_items)}")

    if any_failed and fail_on_failed_assert:
        print(
            "STOP: au moins une fixture a failed-assert > 0. "
            "Les 10 exemples officiels doivent produire 0.",
            file=sys.stderr,
        )
        return 1, digest

    if expected:
        missing = set(expected) - {r["file"] for r in results}
        extra = {r["file"] for r in results} - set(expected)
        if missing or extra:
            print(
                f"ERREUR: ensemble de fixtures != expected.json "
                f"(manquants={sorted(missing)} extra={sorted(extra)})",
                file=sys.stderr,
            )
            return 1, digest
        if drift_items and not allow_fired_drift:
            print(
                "ERREUR: fired-rule != scripts/expected.json "
                "(relancez avec --allow-fired-drift pour accepter l'ecart).",
                file=sys.stderr,
            )
            return 1, digest

    if fail_on_failed_assert:
        print("OK: 10x 0 svrl:failed-assert")
    else:
        n_fail = sum(1 for r in results if r["failed_assert"] > 0)
        n_green = sum(1 for r in results if r["failed_assert"] == 0)
        print(f"OK moteur: {len(results)} fichier(s), {n_fail} avec failed-assert, {n_green} vert(s)")
    return 0, digest


def run_hash_probe(repo: Path, args) -> int:
    mutant_name = args.probe_mutant
    mutant_path = (repo / "mutants" / mutant_name).resolve()
    if not mutant_path.is_file():
        print(f"ERREUR: mutant introuvable : {mutant_path}", file=sys.stderr)
        return 2
    fixtures_dir = repo / "fixtures"
    receipts_dir = repo / "oracles" / "receipts"

    print("=== HASH-PROBE 1/3 : fixtures seulement ===")
    rc1, hash1 = run_validation(
        repo,
        mode=args.mode,
        xml_dir=fixtures_dir,
        receipts_dir=receipts_dir,
        require_integrity=True,
        use_expected=True,
        allow_fired_drift=args.allow_fired_drift,
        fail_on_failed_assert=True,
    )
    print(f"HASH avant : {hash1}")
    if hash1 != EXPECTED_RESULTS_SHA256:
        print(
            f"AVERTISSEMENT: RESULTS.sha256 fixtures != epingle\n"
            f"  attendu {EXPECTED_RESULTS_SHA256}\n"
            f"  obtenu  {hash1}",
            file=sys.stderr,
        )

    print()
    print(f"=== HASH-PROBE 2/3 : 9 originaux + mutant {mutant_name} ===")
    with tempfile.TemporaryDirectory(prefix="en16931-hash-probe-") as td:
        probe_dir = Path(td)
        names = sorted(load_sha256sums(fixtures_dir / "SHA256SUMS"))
        for name in names:
            src = mutant_path if name == mutant_name else fixtures_dir / name
            shutil.copyfile(src, probe_dir / name)
        probe_out = probe_dir / "receipts"
        rc2, hash2 = run_validation(
            repo,
            mode=args.mode,
            xml_dir=probe_dir,
            receipts_dir=probe_out,
            require_integrity=False,
            use_expected=False,
            allow_fired_drift=True,
            fail_on_failed_assert=False,
        )
    print(f"HASH avec mutant : {hash2}")
    if hash2 == hash1:
        print("ERREUR: RESULTS.sha256 n'a PAS change avec le mutant.", file=sys.stderr)
        return 1
    print("OK: RESULTS.sha256 differe lorsque le mutant est dans l'ensemble hashe.")

    print()
    print("=== HASH-PROBE 3/3 : fixtures restaurees (jamais ecrasees) ===")
    rc3, hash3 = run_validation(
        repo,
        mode=args.mode,
        xml_dir=fixtures_dir,
        receipts_dir=receipts_dir,
        require_integrity=True,
        use_expected=True,
        allow_fired_drift=args.allow_fired_drift,
        fail_on_failed_assert=True,
    )
    print(f"HASH apres : {hash3}")
    check_fixtures(repo)
    print("OK: fixtures/SHA256SUMS toujours conforme (originaux intacts).")
    if hash3 != EXPECTED_RESULTS_SHA256:
        print(
            f"ERREUR: hash apres restore != epingle\n"
            f"  attendu {EXPECTED_RESULTS_SHA256}\n"
            f"  obtenu  {hash3}",
            file=sys.stderr,
        )
        return 1
    if hash3 != hash1:
        print("ERREUR: hash apres != hash avant.", file=sys.stderr)
        return 1
    print(f"OK: RESULTS.sha256 revenu a {EXPECTED_RESULTS_SHA256}")
    return 0 if (rc1 == 0 and rc3 == 0) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Valide les 10 fixtures CEN EN16931 1.3.16 (XSLT officiel, SaxonC-HE 13.0)."
    )
    parser.add_argument(
        "--mode",
        choices=("reference", "cross-platform"),
        default="reference",
        help="reference = XSLT vendored (normatif). cross-platform = ZIP officiels si vendor/ absent.",
    )
    parser.add_argument(
        "--allow-fired-drift",
        action="store_true",
        help="Autorise un ecart de fired-rule par rapport a scripts/expected.json (failed-assert doit rester 0).",
    )
    parser.add_argument(
        "--dir",
        default=None,
        help="Repertoire des XML (defaut: fixtures/).",
    )
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Repertoire des recettes SVRL / RESULTS (defaut: oracles/receipts).",
    )
    parser.add_argument(
        "--no-expected",
        action="store_true",
        help="Ignore scripts/expected.json (requis pour les mutants).",
    )
    parser.add_argument(
        "--hash-probe",
        action="store_true",
        help="Prouve que RESULTS.sha256 change si un mutant est dans l'ensemble hashe, puis revient.",
    )
    parser.add_argument(
        "--probe-mutant",
        default="CII_example1.xml",
        help="Nom du mutant pour --hash-probe (defaut: CII_example1.xml).",
    )
    args = parser.parse_args(argv)

    repo = repo_root_from_script()
    fixtures_dir = repo / "fixtures"
    default_out = repo / "oracles" / "receipts"
    xml_dir = resolve_user_path(repo, args.dir, fixtures_dir)
    receipts_dir = resolve_user_path(repo, args.out_dir, default_out)

    if args.hash_probe:
        return run_hash_probe(repo, args)

    default_fixtures = xml_dir.resolve() == fixtures_dir.resolve()
    require_integrity = default_fixtures
    use_expected = (not args.no_expected) and default_fixtures
    fail_on_failed_assert = (not args.no_expected) and default_fixtures
    extra = None
    if not default_fixtures:
        extra = xml_dir

    rc, _digest = run_validation(
        repo,
        mode=args.mode,
        xml_dir=xml_dir,
        receipts_dir=receipts_dir,
        require_integrity=require_integrity,
        use_expected=use_expected,
        allow_fired_drift=args.allow_fired_drift,
        fail_on_failed_assert=fail_on_failed_assert,
        extra_results_dir=extra,
    )
    return rc


if __name__ == "__main__":
    sys.exit(main())
