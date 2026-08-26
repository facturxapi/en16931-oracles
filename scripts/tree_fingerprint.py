#!/usr/bin/env python3
"""Byte fingerprints for versioned artifact trees (checkout-clean guards)."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_tree(root: Path) -> dict[str, str]:
    """Map repo-relative posix paths under root to content sha256."""
    if not root.is_dir():
        return {}
    out: dict[str, str] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        out[rel] = sha256_file(path)
    return out


def diff_fingerprints(before: dict[str, str], after: dict[str, str], *, label: str) -> list[str]:
    errors: list[str] = []
    before_keys = set(before)
    after_keys = set(after)
    for rel in sorted(before_keys - after_keys):
        errors.append(f"{label}: removed {rel}")
    for rel in sorted(after_keys - before_keys):
        errors.append(f"{label}: created {rel}")
    for rel in sorted(before_keys & after_keys):
        if before[rel] != after[rel]:
            errors.append(f"{label}: mutated {rel}")
    return errors
