#!/usr/bin/env python3
"""Offline tests: the drift probe authenticates to the GitHub API only."""

from __future__ import annotations

import email.message
import os
import sys
import unittest
import urllib.request
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import check_upstream  # noqa: E402


class RequestAuthTests(unittest.TestCase):
    API = "https://api.github.com/repos/ConnectingEurope/eInvoicing-EN16931/releases"
    ASSET = "https://github.com/ConnectingEurope/eInvoicing-EN16931/releases/download/validation-1.3.16/en16931-cii-1.3.16.zip"

    def auth(self, url: str, token: str | None) -> str | None:
        env = {} if token is None else {"GITHUB_TOKEN": token}
        with mock.patch.dict(os.environ, env, clear=True):
            request = check_upstream.build_request(url, "ua")
        return request.get_header("Authorization")

    def test_token_sent_to_api_host(self) -> None:
        self.assertEqual(self.auth(self.API, "t0k"), "Bearer t0k")

    def test_token_never_sent_to_asset_download(self) -> None:
        self.assertIsNone(self.auth(self.ASSET, "t0k"))

    def test_no_token_means_anonymous(self) -> None:
        self.assertIsNone(self.auth(self.API, None))

    def test_token_never_sent_over_plain_http(self) -> None:
        self.assertIsNone(self.auth(self.API.replace("https://", "http://"), "t0k"))

    def test_token_never_sent_to_lookalike_hosts(self) -> None:
        for url in (
            "https://api.github.com.evil.example/repos",
            "https://api.github.com@evil.example/repos",
        ):
            self.assertIsNone(self.auth(url, "t0k"), url)

    def test_token_not_replayed_on_redirect(self) -> None:
        with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "t0k"}, clear=True):
            request = check_upstream.build_request(self.API, "ua")
        handler = urllib.request.HTTPRedirectHandler()
        for target in (
            "https://api.github.com/repositories/1/releases",
            "https://objects.githubusercontent.com/x",
            "https://evil.example/x",
        ):
            follow = handler.redirect_request(
                request, None, 302, "Found", email.message.Message(), target
            )
            self.assertIsNone(follow.get_header("Authorization"), target)


if __name__ == "__main__":
    unittest.main()
