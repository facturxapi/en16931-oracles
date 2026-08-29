#!/usr/bin/env python3
"""Polarity gate for BR-CL-08 / BT-21 BAT — must break if CII accept / UBL reject inverts."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
CHECK = REPO / "scripts" / "check_brcl08_polarity.py"
UBL_BAT_STEM = "ubl-tc434-example5-bt21-note-BAT-wrap"
CII_BAT_FILE = "CII_example5-bt21-subject-BAT.xml"
UBL_BAT_FILE = "ubl-tc434-example5-bt21-note-BAT-wrap.xml"
FAILED_BLOCK_RE = re.compile(
    r"<svrl:failed-assert\b[^>]*>.*?</svrl:failed-assert>",
    re.DOTALL,
)


def run_check(root: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["ORACLE_ROOT"] = str(root)
    return subprocess.run(
        [PYTHON, str(root / "scripts" / "check_brcl08_polarity.py")],
        cwd=str(root),
        text=True,
        capture_output=True,
        env=env,
    )


class Brcl08Bt21PolarityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not CHECK.is_file():
            raise unittest.SkipTest("check_brcl08_polarity.py not implemented yet")

    def test_gate_script_exists(self) -> None:
        self.assertTrue(CHECK.is_file())

    def test_polarity_passes_on_committed_tree(self) -> None:
        proc = run_check(REPO)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)

    def test_parent_cii_aai_still_zero_fail(self) -> None:
        svrl = REPO / "oracles" / "receipts" / "CII_example5.svrl.xml"
        text = svrl.read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"<svrl:failed-assert\b", text)), 0)

    def test_mutant_falsified_brcl08_polarity_inverts_fails(self) -> None:
        """Invert CII-accept / UBL-BR-CL-08-reject in copied receipts -> checker must be non-zero."""
        with tempfile.TemporaryDirectory(prefix="brcl08-mutant-polarity-") as td:
            root = Path(td) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
            ubl_svrl = root / "gaps" / "receipts" / f"{UBL_BAT_STEM}.svrl.xml"
            stripped = FAILED_BLOCK_RE.sub("", ubl_svrl.read_text(encoding="utf-8"))
            self.assertNotIn("BR-CL-08", stripped)
            self.assertEqual(len(re.findall(r"<svrl:failed-assert\b", stripped)), 0)
            ubl_svrl.write_text(stripped, encoding="utf-8")

            results_path = root / "gaps" / "receipts" / "RESULTS.json"
            rows = json.loads(results_path.read_text(encoding="utf-8"))
            flipped = 0
            for row in rows:
                if row.get("file") == CII_BAT_FILE:
                    row["failed_assert"] = 1
                    flipped += 1
                elif row.get("file") == UBL_BAT_FILE:
                    row["failed_assert"] = 0
                    flipped += 1
            self.assertEqual(flipped, 2)
            results_path.write_text(
                json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
                + "\n",
                encoding="utf-8",
            )
            gaps_results = root / "gaps" / "RESULTS.json"
            gaps_results.write_text(results_path.read_text(encoding="utf-8"), encoding="utf-8")

            proc = run_check(root)
            self.assertNotEqual(
                proc.returncode,
                0,
                msg="polarity checker must fail when UBL BAT SVRL is 0-fail / BR-CL-08 stripped",
            )


if __name__ == "__main__":
    unittest.main()
