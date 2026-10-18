#!/usr/bin/env python3
"""Polarity gate for BR-CL-08 / BT-21 BAT — causal mutants on the SVRLs the checker reads."""

from __future__ import annotations

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
CII_BAT_SVRL = "CII_example5-bt21-subject-BAT.svrl.xml"
UBL_BAT_SVRL = "ubl-tc434-example5-bt21-note-BAT-wrap.svrl.xml"
UBL_AAI_SVRL = "ubl-tc434-example5-bt21-note-AAI-wrap.svrl.xml"
INJECTED_FAIL = (
    '   <svrl:failed-assert test="false()"'
    ' id="BR-CL-08" flag="fatal" location="/*">'
    "\n      <svrl:text>injected BAT polarity mutant</svrl:text>\n"
    "   </svrl:failed-assert>\n"
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


def copy_repo(td: str) -> Path:
    root = Path(td) / "repo"
    shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".venv", ".git"))
    return root


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

    def test_mutant_cii_bat_accept_to_reject_fails(self) -> None:
        """Checker reads CII BAT SVRL. Inject a real failed-assert -> must fail."""
        with tempfile.TemporaryDirectory(prefix="brcl08-mutant-cii-reject-") as td:
            root = copy_repo(td)
            svrl = root / "gaps" / "receipts" / CII_BAT_SVRL
            text = svrl.read_text(encoding="utf-8")
            self.assertEqual(len(re.findall(r"<svrl:failed-assert\b", text)), 0)
            if "</svrl:schematron-output>" not in text:
                self.fail("CII BAT SVRL missing closing tag")
            mutated = text.replace(
                "</svrl:schematron-output>",
                INJECTED_FAIL + "</svrl:schematron-output>",
                1,
            )
            self.assertGreater(
                len(re.findall(r"<svrl:failed-assert\b", mutated)),
                0,
            )
            svrl.write_text(mutated, encoding="utf-8")
            proc = run_check(root)
            self.assertNotEqual(
                proc.returncode,
                0,
                msg="polarity checker must fail when CII BAT SVRL has a failed-assert\n"
                + (proc.stdout or "")
                + (proc.stderr or ""),
            )

    def inject_and_expect_failure(self, svrl_name: str, label: str) -> None:
        with tempfile.TemporaryDirectory(prefix="brcl08-mutant-") as td:
            root = copy_repo(td)
            svrl = root / "gaps" / "receipts" / svrl_name
            text = svrl.read_text(encoding="utf-8")
            self.assertEqual(len(re.findall(r"<svrl:failed-assert\b", text)), 0)
            self.assertIn("</svrl:schematron-output>", text)
            svrl.write_text(
                text.replace(
                    "</svrl:schematron-output>",
                    INJECTED_FAIL + "</svrl:schematron-output>",
                    1,
                ),
                encoding="utf-8",
            )
            proc = run_check(root)
            self.assertNotEqual(
                proc.returncode,
                0,
                msg=f"polarity checker must fail when {label} SVRL has a failed-assert\n"
                + (proc.stdout or "")
                + (proc.stderr or ""),
            )

    def test_mutant_ubl_bat_accept_to_reject_fails(self) -> None:
        """The 1.3.16 divergence (#510: UBL rejects BAT) coming back must fail."""
        self.inject_and_expect_failure(UBL_BAT_SVRL, "UBL BAT")

    def test_mutant_ubl_aai_accept_to_reject_fails(self) -> None:
        self.inject_and_expect_failure(UBL_AAI_SVRL, "UBL AAI")

if __name__ == "__main__":
    unittest.main()
