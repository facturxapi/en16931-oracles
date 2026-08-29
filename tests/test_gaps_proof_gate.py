#!/usr/bin/env python3
"""Proof gate for gaps/ — must fail until verify_gaps_receipts + hermetic SVRL exist."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VENV_PY = REPO / ".venv" / "bin" / "python"
PYTHON = str(VENV_PY if VENV_PY.is_file() else Path(sys.executable))
VERIFY_GAPS = REPO / "scripts" / "verify_gaps_receipts.py"
GAPS_RECEIPTS = REPO / "gaps" / "receipts"
EXPECTED_GAPS_SHA256 = (
    "f8c43469ba3c0538cf0cabf93f43378c3ed4644e98ef5d118d250b5e8741cef5"
)
GAPS_FIXTURE_COUNT = 30


def run_verify(root: Path, *, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    merged["ORACLE_ROOT"] = str(root)
    if env:
        merged.update(env)
    return subprocess.run(
        [PYTHON, str(VERIFY_GAPS)],
        cwd=str(root),
        text=True,
        capture_output=True,
        env=merged,
    )


class GapsProofGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not VERIFY_GAPS.is_file():
            raise unittest.SkipTest("verify_gaps_receipts.py not implemented yet")

    def test_gate_script_exists(self) -> None:
        self.assertTrue(VERIFY_GAPS.is_file())

    def test_committed_gaps_fixture_count(self) -> None:
        xmls = sorted((REPO / "gaps").glob("*.xml"))
        self.assertEqual(len(xmls), GAPS_FIXTURE_COUNT)

    def test_committed_results_pin(self) -> None:
        pin = (GAPS_RECEIPTS / "RESULTS.sha256").read_text(encoding="utf-8").strip()
        digest, name = pin.split(None, 1)
        self.assertEqual(name, "RESULTS.json")
        self.assertEqual(digest, EXPECTED_GAPS_SHA256)

    def test_verify_gaps_passes_on_clean_tree(self) -> None:
        proc = run_verify(REPO)
        self.assertEqual(
            proc.returncode,
            0,
            msg=proc.stdout + proc.stderr,
        )

    def test_verify_leaves_full_gaps_tree_untouched(self) -> None:
        sys.path.insert(0, str(REPO / "scripts"))
        from tree_fingerprint import fingerprint_tree

        gaps_dir = REPO / "gaps"
        before = fingerprint_tree(gaps_dir)
        proc = run_verify(REPO)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        after = fingerprint_tree(gaps_dir)
        self.assertEqual(before, after)

    def test_gaps_results_copies_are_byte_identical(self) -> None:
        gaps = REPO / "gaps"
        receipts = GAPS_RECEIPTS
        for name in ("RESULTS.json", "RESULTS.sha256"):
            self.assertTrue((gaps / name).read_bytes() == (receipts / name).read_bytes())

    def test_validate_replay_does_not_write_gaps_results(self) -> None:
        gaps_results = REPO / "gaps" / "RESULTS.json"
        before = hashlib.sha256(gaps_results.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix="gaps-nonmut-") as td:
            out = Path(td) / "replay"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(REPO / "scripts" / "validate.py"),
                    "--dir",
                    str(REPO / "gaps"),
                    "--out-dir",
                    str(out),
                    "--no-expected",
                ],
                cwd=str(REPO),
                text=True,
                capture_output=True,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        after = hashlib.sha256(gaps_results.read_bytes()).hexdigest()
        self.assertEqual(before, after)

    def test_mutant_falsified_results_digest_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gaps-mutant-digest-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            pin = root / "gaps" / "receipts" / "RESULTS.sha256"
            pin.write_text("f" * 64 + "  RESULTS.json\n", encoding="utf-8")
            proc = run_verify(root)
            self.assertNotEqual(proc.returncode, 0)

    def test_mutant_falsified_root_results_json_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gaps-mutant-root-json-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            path = root / "gaps" / "RESULTS.json"
            path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            proc = run_verify(root)
            self.assertNotEqual(proc.returncode, 0)

    def test_mutant_falsified_root_results_sha256_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gaps-mutant-root-pin-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            pin = root / "gaps" / "RESULTS.sha256"
            pin.write_text("f" * 64 + "  RESULTS.json\n", encoding="utf-8")
            proc = run_verify(root)
            self.assertNotEqual(proc.returncode, 0)

    def test_mutant_falsified_svrl_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gaps-mutant-svrl-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            svrl = root / "gaps" / "receipts" / "CII_business_example_Z-bt30-X.svrl.xml"
            svrl.write_text(svrl.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            proc = run_verify(root)
            self.assertNotEqual(proc.returncode, 0)

    def test_mutant_falsified_receipt_md_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gaps-mutant-receipt-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            receipt = root / "gaps" / "receipts" / "CII_business_example_Z-bt30-X.receipt.md"
            receipt.write_text(receipt.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            proc = run_verify(root)
            self.assertNotEqual(proc.returncode, 0)

    def test_mutant_falsified_gaps_xml_fails(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gaps-mutant-xml-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            xml = root / "gaps" / "CII_business_example_Z-bt30-X.xml"
            xml.write_text(xml.read_text(encoding="utf-8") + "<!--mutant-->\n", encoding="utf-8")
            proc = run_verify(root)
            self.assertNotEqual(proc.returncode, 0)

    def test_two_absolute_checkouts_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory(prefix="gaps-hermetic-") as td:
            checkout_a = Path(td) / "checkout-a" / "en16931-oracles"
            checkout_b = Path(td) / "checkout-b" / "en16931-oracles"
            ignore = shutil.ignore_patterns(".venv", ".git")
            shutil.copytree(REPO, checkout_a, ignore=ignore)
            shutil.copytree(REPO, checkout_b, ignore=ignore)
            out_a = checkout_a / "_replay"
            out_b = checkout_b / "_replay"
            for root, out in ((checkout_a, out_a), (checkout_b, out_b)):
                proc = subprocess.run(
                    [
                        PYTHON,
                        str(root / "scripts" / "validate.py"),
                        "--dir",
                        str(root / "gaps"),
                        "--out-dir",
                        str(out),
                        "--no-expected",
                    ],
                    cwd=str(root),
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(
                    proc.returncode,
                    0,
                    msg=(proc.stdout or "") + (proc.stderr or ""),
                )
            names = sorted(p.name for p in out_a.iterdir())
            self.assertEqual(names, sorted(p.name for p in out_b.iterdir()))
            for name in names:
                a = (out_a / name).read_bytes()
                b = (out_b / name).read_bytes()
                self.assertEqual(
                    a,
                    b,
                    msg=(
                        f"byte mismatch for {name} "
                        f"(sha256 a={hashlib.sha256(a).hexdigest()} "
                        f"b={hashlib.sha256(b).hexdigest()})"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
