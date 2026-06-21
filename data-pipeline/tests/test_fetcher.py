"""
============================================================
TESTS — Pipeline Layer 1: Fetcher
============================================================
Run with:  python tests/test_fetcher.py

These tests do NOT make a real network call to Reddit. Instead,
we "mock" (fake) the requests.get() function so we can test our
own code's behavior — like which URL and headers we send —
without depending on the internet or Reddit's servers being up.

This is a standard testing technique: you don't need to test that
`requests` works (that's the library's job), you need to test
that YOUR code calls it correctly.
============================================================
"""

import sys
import os
import json
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.fetcher import fetch_top_posts_raw, REDDIT_TOP_URL, USER_AGENT

# ─────────────────────────────────────────────
# TEST RUNNER HELPER
# ─────────────────────────────────────────────

passed = 0
failed = 0

def assert_that(label: str, condition: bool) -> None:
    global passed, failed
    if condition:
        print(f"  ✅ PASS — {label}")
        passed += 1
    else:
        print(f"  ❌ FAIL — {label}")
        failed += 1

# ─────────────────────────────────────────────
# LOAD FIXTURE DATA (the FAKE response Reddit "sends back")
# ─────────────────────────────────────────────

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "sample_reddit_response.json")
with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
    FAKE_REDDIT_RESPONSE = json.load(f)

# ─────────────────────────────────────────────
# TEST A — fetch_top_posts_raw() calls requests.get correctly
# ─────────────────────────────────────────────

print("TEST A: fetch_top_posts_raw() sends the right request")

with patch("pipeline.fetcher.requests.get") as mock_get:
    # Configure the fake response object
    mock_response = Mock()
    mock_response.json.return_value = FAKE_REDDIT_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_top_posts_raw(time_filter="month", limit=10)

    # Was requests.get() called at all?
    assert_that("requests.get was called exactly once", mock_get.call_count == 1)

    # What arguments was it called with?
    call_args, call_kwargs = mock_get.call_args

    assert_that("Called the correct Reddit URL", call_args[0] == REDDIT_TOP_URL or call_kwargs.get("url") == REDDIT_TOP_URL)
    assert_that("Sent a User-Agent header", call_kwargs.get("headers", {}).get("User-Agent") == USER_AGENT)
    assert_that("Sent t=month in params", call_kwargs.get("params", {}).get("t") == "month")
    assert_that("Sent limit=10 in params", call_kwargs.get("params", {}).get("limit") == 10)
    assert_that("Called raise_for_status() to check for errors", mock_response.raise_for_status.called)
    assert_that("Returned the parsed JSON", result == FAKE_REDDIT_RESPONSE)

print()

# ─────────────────────────────────────────────
# TEST B — fetch_top_posts_raw() uses default arguments
# ─────────────────────────────────────────────

print("TEST B: fetch_top_posts_raw() works with default arguments")

with patch("pipeline.fetcher.requests.get") as mock_get:
    mock_response = Mock()
    mock_response.json.return_value = FAKE_REDDIT_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_top_posts_raw()  # no arguments — should use defaults

    assert_that("Still calls requests.get with no errors", mock_get.call_count == 1)
    assert_that("Returns the JSON correctly", result == FAKE_REDDIT_RESPONSE)

print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All fetcher tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in pipeline/fetcher.py")
