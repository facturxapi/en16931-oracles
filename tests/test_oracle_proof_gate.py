#!/usr/bin/env python3
"""Proof gate for official oracles/receipts — non-mutating replay."""

from __future__ import annotations

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
VERIFY_ORACLES = REPO / "scripts" / "verify_receipts.py"
ORACLE_RECEIPTS = REPO / "oracles" / "receipts"


def run_verify(root: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["ORACLE_ROOT"] = str(root)
    return subprocess.run(
        [PYTHON, str(VERIFY_ORACLES)],
        cwd=str(root),
        text=True,
        capture_output=True,
        env=env,
    )


class OracleProofGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not VERIFY_ORACLES.is_file():
            raise unittest.SkipTest("verify_receipts.py not implemented yet")

    def test_verify_oracles_passes_on_clean_tree(self) -> None:
        proc = run_verify(REPO)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)

    def test_verify_leaves_oracles_receipts_tree_untouched(self) -> None:
        sys.path.insert(0, str(REPO / "scripts"))
        from tree_fingerprint import fingerprint_tree

        before = fingerprint_tree(ORACLE_RECEIPTS)
        proc = run_verify(REPO)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        after = fingerprint_tree(ORACLE_RECEIPTS)
        self.assertEqual(before, after)

    def test_mutant_falsified_oracle_svrl_not_auto_repaired(self) -> None:
        with tempfile.TemporaryDirectory(prefix="oracle-mutant-svrl-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            svrl = root / "oracles" / "receipts" / "CII_example1.svrl.xml"
            original = svrl.read_bytes()
            mutated = original + b"MUTANT\n"
            svrl.write_bytes(mutated)
            proc = run_verify(root)
            self.assertNotEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            self.assertEqual(svrl.read_bytes(), mutated)


if __name__ == "__main__":
    unittest.main()
