#!/usr/bin/env python3
"""Hermetic SVRL document URI helpers shared by validate.py and verify gates."""

from __future__ import annotations

import re
from pathlib import Path

SVRL_DOC_ATTR_RE = re.compile(r'\b(document|documents)="([^"]+)"')
SVRL_FILE_URI_TAIL_RE = re.compile(r"^file:(.+)$")


def expected_document_uri(fixture_xml_name: str) -> str:
    return f"file:{Path(fixture_xml_name).name}"


def fixture_xml_name_from_svrl_path(svrl_path: Path) -> str:
    name = svrl_path.name
    if not name.endswith(".svrl.xml"):
        raise ValueError(f"not an SVRL receipt path: {svrl_path}")
    return name[: -len(".svrl.xml")] + ".xml"


def iter_document_uris(svrl: str) -> list[tuple[str, str]]:
    return [(m.group(1), m.group(2)) for m in SVRL_DOC_ATTR_RE.finditer(svrl)]


def validate_document_uris(svrl: str, fixture_xml_name: str) -> list[str]:
    """Positive check: every document/documents URI is exactly file:<basename>."""
    expected = expected_document_uri(fixture_xml_name)
    errors: list[str] = []
    seen = iter_document_uris(svrl)
    if not seen:
        errors.append(f"no document/documents URI attributes for {fixture_xml_name}")
        return errors
    for attr, uri in seen:
        if uri != expected:
            errors.append(
                f"{attr}={uri!r} != expected {expected!r} for {fixture_xml_name}"
            )
    return errors


def hermeticize_svrl(svrl: str, fixture_xml_name: str) -> str:
    """Normalize Saxon file URIs to file:<basename>; fail on mismatch."""
    expected = expected_document_uri(fixture_xml_name)
    errors: list[str] = []

    def repl(match: re.Match[str]) -> str:
        attr, uri = match.group(1), match.group(2)
        tail = SVRL_FILE_URI_TAIL_RE.match(uri)
        if tail is None:
            errors.append(f"{attr}={uri!r} is not a file: URI for {fixture_xml_name}")
            return match.group(0)
        ref = tail.group(1).replace("\\", "/")
        basename = Path(ref).name
        if basename != Path(fixture_xml_name).name:
            errors.append(
                f"{attr}={uri!r} basename {basename!r} != {fixture_xml_name!r}"
            )
            return match.group(0)
        return f'{attr}="{expected}"'

    normalized = SVRL_DOC_ATTR_RE.sub(repl, svrl)
    if errors:
        detail = "; ".join(errors)
        raise ValueError(
            f"SVRL document URI mismatch for {fixture_xml_name}: {detail}"
        )
    post_errors = validate_document_uris(normalized, fixture_xml_name)
    if post_errors:
        raise ValueError(
            f"SVRL hermeticization incomplete for {fixture_xml_name}: "
            + "; ".join(post_errors)
        )
    return normalized
