#!/usr/bin/env python3
"""variants/533: probes are reproducible from the pinned fixtures, artifacts are pinned."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
V533 = REPO / "variants" / "533"


class Variants533(unittest.TestCase):
    def test_probes_regenerate_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(REPO / "fixtures", root / "fixtures")
            subprocess.run(
                [sys.executable, "-I", str(V533 / "make_probes.py"), str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            made = sorted(p.relative_to(root / "variants/533/probes") for p in (root / "variants/533/probes").rglob("*.xml"))
            committed = sorted(p.relative_to(V533 / "probes") for p in (V533 / "probes").rglob("*.xml"))
            self.assertEqual(made, committed)
            self.assertEqual(len(made), 32)
            for rel in made:
                self.assertEqual(
                    (root / "variants/533/probes" / rel).read_bytes(),
                    (V533 / "probes" / rel).read_bytes(),
                    str(rel),
                )

    def test_xslt_pinned(self) -> None:
        for line in (V533 / "xslt" / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
            digest, name = line.split()
            actual = hashlib.sha256((V533 / "xslt" / name).read_bytes()).hexdigest()
            self.assertEqual(actual, digest, name)


if __name__ == "__main__":
    unittest.main()
