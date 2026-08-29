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
FAILED_BLOCK_RE = re.compile(
    r"<svrl:failed-assert\b[^>]*>.*?</svrl:failed-assert>",
    re.DOTALL,
)
ID_ATTR_RE = re.compile(r'\bid="([^"]+)"')
FLAG_ATTR_RE = re.compile(r'\bflag="([^"]+)"')
INJECTED_FAIL = (
    '   <svrl:failed-assert test="false()"'
    ' id="BR-CL-08" flag="fatal" location="/*">'
    "\n      <svrl:text>injected CII BAT polarity mutant</svrl:text>\n"
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


def ubl_failed_open(text: str) -> re.Match[str]:
    m = re.search(r"<svrl:failed-assert\b[^>]*>", text, re.DOTALL)
    if m is None:
        raise AssertionError("UBL BAT SVRL has no failed-assert to mutate")
    return m


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

    def test_mutant_ubl_bat_reject_to_accept_fails(self) -> None:
        """Strip the UBL BAT failed-assert BR-CL-08 the checker parses -> must fail."""
        with tempfile.TemporaryDirectory(prefix="brcl08-mutant-ubl-accept-") as td:
            root = copy_repo(td)
            svrl = root / "gaps" / "receipts" / UBL_BAT_SVRL
            original = svrl.read_text(encoding="utf-8")
            self.assertIn("BR-CL-08", original)
            stripped = FAILED_BLOCK_RE.sub("", original)
            self.assertNotIn("BR-CL-08", stripped)
            self.assertEqual(len(re.findall(r"<svrl:failed-assert\b", stripped)), 0)
            svrl.write_text(stripped, encoding="utf-8")
            proc = run_check(root)
            self.assertNotEqual(
                proc.returncode,
                0,
                msg="polarity checker must fail when UBL BAT SVRL has 0 failed-assert\n"
                + (proc.stdout or "")
                + (proc.stderr or ""),
            )

    def test_mutant_ubl_bat_wrong_rule_id_fails(self) -> None:
        """Keep a failed-assert, replace BR-CL-08 with another id -> must fail."""
        with tempfile.TemporaryDirectory(prefix="brcl08-mutant-ubl-id-") as td:
            root = copy_repo(td)
            svrl = root / "gaps" / "receipts" / UBL_BAT_SVRL
            original = svrl.read_text(encoding="utf-8")
            opening = ubl_failed_open(original)
            attrs = opening.group(0)
            im = ID_ATTR_RE.search(attrs)
            self.assertIsNotNone(im)
            self.assertEqual(im.group(1), "BR-CL-08")
            new_open = attrs.replace('id="BR-CL-08"', 'id="BR-CL-15"', 1)
            mutated = original[: opening.start()] + new_open + original[opening.end() :]
            self.assertIn('id="BR-CL-15"', mutated)
            self.assertNotIn('id="BR-CL-08"', mutated)
            self.assertEqual(len(re.findall(r"<svrl:failed-assert\b", mutated)), 1)
            svrl.write_text(mutated, encoding="utf-8")
            proc = run_check(root)
            self.assertNotEqual(
                proc.returncode,
                0,
                msg="polarity checker must fail when UBL BAT failed-assert id is not BR-CL-08\n"
                + (proc.stdout or "")
                + (proc.stderr or ""),
            )

    def test_mutant_ubl_bat_wrong_flag_fails(self) -> None:
        """Keep id BR-CL-08, replace flag=fatal with a wrong flag -> must fail."""
        with tempfile.TemporaryDirectory(prefix="brcl08-mutant-ubl-flag-") as td:
            root = copy_repo(td)
            svrl = root / "gaps" / "receipts" / UBL_BAT_SVRL
            original = svrl.read_text(encoding="utf-8")
            opening = ubl_failed_open(original)
            attrs = opening.group(0)
            fm = FLAG_ATTR_RE.search(attrs)
            self.assertIsNotNone(fm)
            self.assertEqual(fm.group(1), "fatal")
            new_open = attrs.replace('flag="fatal"', 'flag="warning"', 1)
            mutated = original[: opening.start()] + new_open + original[opening.end() :]
            self.assertIn('id="BR-CL-08"', mutated)
            self.assertIn('flag="warning"', mutated)
            self.assertNotIn('flag="fatal"', mutated)
            self.assertEqual(len(re.findall(r"<svrl:failed-assert\b", mutated)), 1)
            svrl.write_text(mutated, encoding="utf-8")
            proc = run_check(root)
            self.assertNotEqual(
                proc.returncode,
                0,
                msg="polarity checker must fail when UBL BAT BR-CL-08 flag is not fatal\n"
                + (proc.stdout or "")
                + (proc.stderr or ""),
            )


if __name__ == "__main__":
    unittest.main()
