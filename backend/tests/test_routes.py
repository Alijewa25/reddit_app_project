"""
============================================================
TESTS — Backend Layer 3: API Routes
============================================================
Run with:  python tests/test_routes.py

We use Flask's built-in test client to send fake HTTP requests
to our app, without needing to actually start a server on a port.

The service layer is mocked, so these tests check ONLY that routes
handle requests/responses correctly (status codes, JSON shape) —
not the underlying business logic (that's test_service.py's job).
============================================================
"""

import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.routes import app

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

client = app.test_client()

# ─────────────────────────────────────────────
# TEST A — GET /api/health (already implemented, sanity check)
# ─────────────────────────────────────────────

print("TEST A: GET /api/health")

response = client.get("/api/health")
assert_that("Status code is 200", response.status_code == 200)
assert_that("success is True", response.get_json()["success"] is True)

print()

# ─────────────────────────────────────────────
# TEST B — GET /api/posts/top
# ─────────────────────────────────────────────

print("TEST B: GET /api/posts/top")

fake_result = {"success": True, "data": [{"title": "Fake Post"}], "count": 1}
with patch("app.routes.service.get_top_posts_for_api", return_value=fake_result) as mock_service:
    response = client.get("/api/posts/top")
    assert_that("Status code is 200", response.status_code == 200)
    assert_that("Response JSON matches service output", response.get_json() == fake_result)
    assert_that("Service called with default limit=10", mock_service.call_args[0][0] == 10)

with patch("app.routes.service.get_top_posts_for_api", return_value=fake_result) as mock_service:
    response = client.get("/api/posts/top?limit=5")
    assert_that("limit query param is passed through as int", mock_service.call_args[0][0] == 5)

print()

# ─────────────────────────────────────────────
# TEST C — GET /api/posts/<post_id>
# ─────────────────────────────────────────────

print("TEST C: GET /api/posts/<post_id>")

found_result = {"success": True, "data": {"title": "Found Post"}}
with patch("app.routes.service.get_single_post_for_api", return_value=found_result):
    response = client.get("/api/posts/t3_abc123")
    assert_that("Status code is 200 when found", response.status_code == 200)
    assert_that("Returns the post data", response.get_json()["data"]["title"] == "Found Post")

not_found_result = {"success": False, "error": "Post not found."}
with patch("app.routes.service.get_single_post_for_api", return_value=not_found_result):
    response = client.get("/api/posts/t3_missing")
    assert_that("Status code is 404 when not found", response.status_code == 404)
    assert_that("Returns success: False", response.get_json()["success"] is False)

print()

# ─────────────────────────────────────────────
# TEST D — GET /api/stats
# ─────────────────────────────────────────────

print("TEST D: GET /api/stats")

stats_result = {"success": True, "data": {"total_posts": 7}}
with patch("app.routes.service.get_stats_for_api", return_value=stats_result):
    response = client.get("/api/stats")
    assert_that("Status code is 200", response.status_code == 200)
    assert_that("total_posts is correct", response.get_json()["data"]["total_posts"] == 7)

print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All route tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in app/routes.py")
