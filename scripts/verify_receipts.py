#!/usr/bin/env python3
"""Re-execute the 10 official EN16931 oracle receipts and compare pinned artifacts.

Runnable outside GitHub Actions. Set ORACLE_ROOT to the public-repo checkout
root. The gate is strictly non-mutating: replay writes only to a temp directory.
Does not call a remote validator. Never logs invoice bytes.
"""

from __future__ import annotations

import filecmp
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from svrl_hermetic import fixture_xml_name_from_svrl_path, validate_document_uris
from tree_fingerprint import diff_fingerprints, fingerprint_tree, sha256_file

EXPECTED_RESULTS_SHA256 = (
    "dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab"
)
FIXTURE_COUNT = 10
EXIT_OK = 0
EXIT_DIVERGE = 1
EXIT_CONFIG = 2


def oracle_root() -> Path:
    raw = os.environ.get("ORACLE_ROOT")
    if raw:
        return Path(raw)
    return Path.cwd()


def write_summary(lines: list[str]) -> None:
    text = "\n".join(lines) + "\n"
    print(text, end="")
    dest = os.environ.get("GITHUB_STEP_SUMMARY")
    if dest:
        with open(dest, "a", encoding="utf-8") as handle:
            handle.write(text)


def check_fixture_sums(root: Path) -> list[str]:
    sums = root / "fixtures" / "SHA256SUMS"
    if not sums.is_file():
        return [f"missing {sums.name}"]
    errors: list[str] = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, name = line.split(None, 1)
        path = root / "fixtures" / name
        if not path.is_file():
            errors.append(f"missing fixture {name}")
            continue
        got = sha256_file(path)
        if got != digest:
            errors.append(f"{name}: fixture sha {got} != {digest}")
    return errors


def check_results_pin(receipts: Path) -> list[str]:
    results = receipts / "RESULTS.json"
    pin = receipts / "RESULTS.sha256"
    errors: list[str] = []
    if not results.is_file():
        return ["missing oracles/receipts/RESULTS.json"]
    if not pin.is_file():
        return ["missing oracles/receipts/RESULTS.sha256"]
    line = pin.read_text(encoding="utf-8").strip()
    digest, name = line.split(None, 1)
    if name != "RESULTS.json":
        errors.append(f"RESULTS.sha256 names {name!r}, expected RESULTS.json")
    if digest != EXPECTED_RESULTS_SHA256:
        errors.append(
            f"RESULTS.sha256 pin {digest} != expected {EXPECTED_RESULTS_SHA256}"
        )
    got = sha256_file(results)
    if got != digest:
        errors.append(f"RESULTS.json sha {got} != pin {digest}")
    return errors


def rerun_validate(root: Path, out_dir: Path) -> int:
    script = root / "scripts" / "validate.py"
    if not script.is_file():
        write_summary(["## Receipts — config", "", "scripts/validate.py is missing"])
        return EXIT_CONFIG
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--mode",
            "reference",
            "--dir",
            str(root / "fixtures"),
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(root),
        text=True,
    )
    return completed.returncode


def compare_receipt_trees(pinned: Path, replay: Path) -> list[str]:
    errors: list[str] = []
    pinned_names = {p.name for p in pinned.iterdir() if p.is_file()}
    replay_names = {p.name for p in replay.iterdir() if p.is_file()}
    missing = sorted(pinned_names - replay_names)
    extra = sorted(replay_names - pinned_names)
    if missing:
        errors.append(f"replay missing artifacts: {missing}")
    if extra:
        errors.append(f"replay has unexpected artifacts: {extra}")
    for name in sorted(pinned_names & replay_names):
        if not filecmp.cmp(pinned / name, replay / name, shallow=False):
            errors.append(f"artifact diverged: {name}")
    return errors


def check_svrl_hermetic_uris(receipts: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(receipts.glob("*.svrl.xml")):
        fixture = fixture_xml_name_from_svrl_path(path)
        errors.extend(
            f"{path.name}: {msg}"
            for msg in validate_document_uris(path.read_text(encoding="utf-8"), fixture)
        )
    return errors


def main() -> int:
    root = oracle_root()
    receipts = root / "oracles" / "receipts"
    diverged: list[str] = []

    diverged.extend(check_fixture_sums(root))
    diverged.extend(check_results_pin(receipts))
    diverged.extend(check_svrl_hermetic_uris(receipts))

    before_receipts = fingerprint_tree(receipts)
    with tempfile.TemporaryDirectory(prefix="en16931-oracle-replay-") as td:
        replay_dir = Path(td) / "receipts"
        rc = rerun_validate(root, replay_dir)
        if rc == EXIT_CONFIG:
            return EXIT_CONFIG
        if rc != 0:
            diverged.append(f"scripts/validate.py --mode reference exited {rc}")
        diverged.extend(compare_receipt_trees(receipts, replay_dir))

    diverged.extend(
        diff_fingerprints(before_receipts, fingerprint_tree(receipts), label="oracles/receipts")
    )

    if diverged:
        write_summary(
            [
                "## Receipts — DIVERGED",
                "",
                *[f"- {item}" for item in diverged],
            ]
        )
        return EXIT_DIVERGE

    write_summary(
        [
            "## Receipts — OK",
            "",
            f"- {FIXTURE_COUNT} fixture SHA256SUMS match",
            "- non-mutating replay matches all pinned SVRL/receipt artifacts",
            f"- RESULTS.sha256 = `{EXPECTED_RESULTS_SHA256}`",
            "- oracles/receipts tree fingerprint unchanged",
        ]
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
