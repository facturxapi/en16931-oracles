#!/usr/bin/env python3
"""Re-execute the 10 official EN16931 oracle receipts and check RESULTS.sha256.

Runnable outside GitHub Actions. Set ORACLE_ROOT to the public-repo checkout
(the directory that contains fixtures/, SHA256SUMS, scripts/validate.py, and
oracles/receipts/RESULTS.sha256). Defaults to the current working directory
so the same script works after it is deposited in the public repo.

Does not call a remote validator. Never logs invoice bytes.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

EXPECTED_RESULTS_SHA256 = (
    "dffb88780654fb4861df84bbd6df18aae5d89b0a5b8f4fd12ce5fb5f9a7f0dab"
)
EXIT_OK = 0
EXIT_DIVERGE = 1
EXIT_CONFIG = 2


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
    sums = root / "SHA256SUMS"
    if not sums.is_file():
        return [f"missing {sums.name}"]
    errors: list[str] = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, name = line.split(None, 1)
        path = root / name
        if not path.is_file():
            errors.append(f"missing fixture {name}")
            continue
        got = sha256_file(path)
        if got != digest:
            errors.append(f"{name}: fixture sha {got} != {digest}")
    return errors


def rerun_validate(root: Path) -> int:
    script = root / "scripts" / "validate.py"
    if not script.is_file():
        write_summary(["## Receipts — config", "", "scripts/validate.py is missing"])
        return EXIT_CONFIG
    completed = subprocess.run(
        [sys.executable, str(script), "--mode", "reference"],
        cwd=str(root),
        text=True,
    )
    return completed.returncode


def check_results(root: Path) -> list[str]:
    receipts = root / "oracles" / "receipts"
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


def main() -> int:
    root = oracle_root()
    diverged: list[str] = []
    fixture_errors = check_fixture_sums(root)
    diverged.extend(fixture_errors)
    rc = rerun_validate(root)
    if rc == EXIT_CONFIG:
        return EXIT_CONFIG
    if rc != 0:
        diverged.append(f"scripts/validate.py --mode reference exited {rc}")
    diverged.extend(check_results(root))
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
            f"- 10 fixture SHA256SUMS match",
            f"- scripts/validate.py --mode reference exited 0",
            f"- RESULTS.sha256 = `{EXPECTED_RESULTS_SHA256}`",
        ]
    )
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
