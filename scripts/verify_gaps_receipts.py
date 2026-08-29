#!/usr/bin/env python3
"""Re-execute gaps/ probes and compare pinned RESULTS + all SVRL/receipt artifacts.

Runnable outside GitHub Actions. Set ORACLE_ROOT to the repo checkout root.
Does not call a remote validator. Never logs invoice bytes.
The gate is strictly non-mutating: replay writes only to a temp directory.
"""

from __future__ import annotations

import filecmp
import os
import subprocess
import sys
import tempfile
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))
from svrl_hermetic import (
    fixture_xml_name_from_svrl_path,
    validate_document_uris,
)
from tree_fingerprint import diff_fingerprints, fingerprint_tree, sha256_file

EXPECTED_GAPS_RESULTS_SHA256 = (
    "9e42443b4b014a46f24705b24c4e8100ddd8e142e3f754c4bc191b2581e701e1"
)
GAPS_FIXTURE_COUNT = 27
RESULTS_NAMES = ("RESULTS.json", "RESULTS.sha256")
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


def count_gaps_fixtures(root: Path) -> int:
    gaps = root / "gaps"
    if not gaps.is_dir():
        return 0
    return sum(1 for p in gaps.iterdir() if p.is_file() and p.suffix.lower() == ".xml")


def check_results_pin(results_dir: Path, *, label: str) -> list[str]:
    results = results_dir / "RESULTS.json"
    pin = results_dir / "RESULTS.sha256"
    errors: list[str] = []
    if not results.is_file():
        return [f"missing {label}/{results.name}"]
    if not pin.is_file():
        return [f"missing {label}/{pin.name}"]
    line = pin.read_text(encoding="utf-8").strip()
    digest, name = line.split(None, 1)
    if name != "RESULTS.json":
        errors.append(f"{label} RESULTS.sha256 names {name!r}, expected RESULTS.json")
    if results_dir.name == "receipts" and digest != EXPECTED_GAPS_RESULTS_SHA256:
        errors.append(
            f"{label} RESULTS.sha256 pin {digest} != expected {EXPECTED_GAPS_RESULTS_SHA256}"
        )
    got = sha256_file(results)
    if got != digest:
        errors.append(f"{label} RESULTS.json sha {got} != pin {digest}")
    return errors


def check_results_copies_match(gaps_dir: Path, receipts_dir: Path) -> list[str]:
    errors: list[str] = []
    for name in RESULTS_NAMES:
        a = gaps_dir / name
        b = receipts_dir / name
        if not a.is_file():
            errors.append(f"missing gaps/{name}")
            continue
        if not b.is_file():
            errors.append(f"missing gaps/receipts/{name}")
            continue
        if not filecmp.cmp(a, b, shallow=False):
            errors.append(f"gaps/{name} != gaps/receipts/{name}")
    return errors


def rerun_gaps_validate(root: Path, out_dir: Path) -> int:
    script = root / "scripts" / "validate.py"
    if not script.is_file():
        write_summary(["## Gaps receipts — config", "", "scripts/validate.py is missing"])
        return EXIT_CONFIG
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--mode",
            "reference",
            "--dir",
            str(root / "gaps"),
            "--out-dir",
            str(out_dir),
            "--no-expected",
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
    gaps_dir = root / "gaps"
    receipts = gaps_dir / "receipts"
    diverged: list[str] = []

    fixture_count = count_gaps_fixtures(root)
    if fixture_count != GAPS_FIXTURE_COUNT:
        diverged.append(
            f"gaps fixture count {fixture_count} != expected {GAPS_FIXTURE_COUNT}"
        )

    diverged.extend(check_results_pin(receipts, label="gaps/receipts"))
    diverged.extend(check_results_pin(gaps_dir, label="gaps"))
    diverged.extend(check_results_copies_match(gaps_dir, receipts))
    diverged.extend(check_svrl_hermetic_uris(receipts))

    before_gaps = fingerprint_tree(gaps_dir)
    with tempfile.TemporaryDirectory(prefix="en16931-gaps-replay-") as td:
        replay_dir = Path(td) / "receipts"
        rc = rerun_gaps_validate(root, replay_dir)
        if rc == EXIT_CONFIG:
            return EXIT_CONFIG
        if rc != 0:
            diverged.append(f"scripts/validate.py gaps replay exited {rc}")
        diverged.extend(compare_receipt_trees(receipts, replay_dir))
        diverged.extend(check_results_pin(replay_dir, label="replay"))
        for name in RESULTS_NAMES:
            pinned = receipts / name
            replayed = replay_dir / name
            if pinned.is_file() and replayed.is_file() and not filecmp.cmp(
                pinned, replayed, shallow=False
            ):
                diverged.append(f"replay {name} != pinned gaps/receipts/{name}")

    diverged.extend(
        diff_fingerprints(before_gaps, fingerprint_tree(gaps_dir), label="gaps")
    )

    if diverged:
        write_summary(
            [
                "## Gaps receipts — DIVERGED",
                "",
                *[f"- {item}" for item in diverged],
            ]
        )
        return EXIT_DIVERGE

    write_summary(
        [
            "## Gaps receipts — OK",
            "",
            f"- {GAPS_FIXTURE_COUNT} gaps fixtures replayed (non-mutating)",
            f"- gaps RESULTS.sha256 = `{EXPECTED_GAPS_RESULTS_SHA256}`",
            "- gaps/RESULTS.* byte-identical to gaps/receipts/RESULTS.*",
            "- all gaps SVRL + receipt.md artifacts byte-stable",
            "- every SVRL document URI is exactly file:<basename.xml>",
            "- full gaps/ tree fingerprint unchanged",
        ]
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
