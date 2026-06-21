"""
============================================================
TESTS — Backend Layer 2: Service
============================================================
Run with:  python tests/test_service.py

These tests MOCK (fake) the repository layer entirely. This means
we are testing ONLY the service's logic — formatting, clamping
limits, handling "not found" — without touching any real database.

This is the benefit of layered architecture: each layer can be
tested in total isolation from the ones below it.
============================================================
"""

import sys
import os
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import service

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
# HELPER: build a fake Post-like object
# ─────────────────────────────────────────────

def make_fake_post(post_id, title, score):
    fake = Mock()
    fake.to_dict.return_value = {
        "id": 1,
        "post_id": post_id,
        "title": title,
        "author": "fake_author",
        "score": score,
        "num_comments": 10,
        "url": "https://example.com",
        "permalink": "https://www.reddit.com/r/programming/fake/",
        "created_utc": 1716000000.0,
        "fetched_at": "2024-01-01T00:00:00+00:00",
    }
    return fake

# ─────────────────────────────────────────────
# TEST A — get_top_posts_for_api() happy path
# ─────────────────────────────────────────────

print("TEST A: get_top_posts_for_api() with normal limit")

fake_posts = [make_fake_post("t3_a", "Post A", 100), make_fake_post("t3_b", "Post B", 50)]

with patch("app.service.repository.get_top_posts", return_value=fake_posts) as mock_repo:
    result = service.get_top_posts_for_api(limit=10)

    assert_that("repository.get_top_posts was called once", mock_repo.call_count == 1)
    assert_that("success is True", result["success"] is True)
    assert_that("data is a list of dicts", all(isinstance(p, dict) for p in result["data"]))
    assert_that("data has 2 posts", len(result["data"]) == 2)
    assert_that("count matches data length", result["count"] == 2)
    assert_that("first post title is correct", result["data"][0]["title"] == "Post A")

print()

# ─────────────────────────────────────────────
# TEST B — get_top_posts_for_api() clamps limit
# ─────────────────────────────────────────────

print("TEST B: get_top_posts_for_api() clamps out-of-range limits")

with patch("app.service.repository.get_top_posts", return_value=[]) as mock_repo:
    service.get_top_posts_for_api(limit=0)
    called_limit = mock_repo.call_args[0][0] if mock_repo.call_args[0] else mock_repo.call_args[1].get("limit")
    assert_that("limit=0 gets clamped up to at least 1", called_limit >= 1)

with patch("app.service.repository.get_top_posts", return_value=[]) as mock_repo:
    service.get_top_posts_for_api(limit=500)
    called_limit = mock_repo.call_args[0][0] if mock_repo.call_args[0] else mock_repo.call_args[1].get("limit")
    assert_that("limit=500 gets clamped down to 50 or less", called_limit <= 50)

print()

# ─────────────────────────────────────────────
# TEST C — get_single_post_for_api() found vs not found
# ─────────────────────────────────────────────

print("TEST C: get_single_post_for_api()")

fake_post = make_fake_post("t3_x", "Found Post", 777)

with patch("app.service.repository.get_post_by_id", return_value=fake_post):
    result = service.get_single_post_for_api("t3_x")
    assert_that("success is True when post exists", result["success"] is True)
    assert_that("data is a dict", isinstance(result["data"], dict))
    assert_that("data title matches", result["data"]["title"] == "Found Post")

with patch("app.service.repository.get_post_by_id", return_value=None):
    result = service.get_single_post_for_api("t3_missing")
    assert_that("success is False when post is missing", result["success"] is False)
    assert_that("error message is a string", isinstance(result["error"], str))

print()

# ─────────────────────────────────────────────
# TEST D — get_stats_for_api()
# ─────────────────────────────────────────────

print("TEST D: get_stats_for_api()")

with patch("app.service.repository.count_posts", return_value=42):
    result = service.get_stats_for_api()
    assert_that("success is True", result["success"] is True)
    assert_that("total_posts matches mocked count", result["data"]["total_posts"] == 42)

print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All service tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in app/service.py")
