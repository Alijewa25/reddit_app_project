"""
============================================================
TESTS — Pipeline Layer 2: Transformer
============================================================
Run with:  python tests/test_transformer.py

These tests use a saved sample JSON file (sample_reddit_response.json)
instead of hitting the real Reddit API. This means:
  - Tests run instantly
  - Tests work without internet access
  - Tests give the same result every time

This is a common pattern: save a real example of the data once,
then test your transformation logic against that fixed example.
============================================================
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.transformer import transform_post, transform_posts

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
# LOAD FIXTURE DATA
# ─────────────────────────────────────────────

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "sample_reddit_response.json")
with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
    SAMPLE_RAW_JSON = json.load(f)

SAMPLE_SINGLE_POST = SAMPLE_RAW_JSON["data"]["children"][0]["data"]

# ─────────────────────────────────────────────
# TEST A — transform_post() on a single post
# ─────────────────────────────────────────────

print("TEST A: transform_post() with one raw post")

result = transform_post(SAMPLE_SINGLE_POST)

assert_that("Returns a dict", isinstance(result, dict))
assert_that("post_id has t3_ prefix", result["post_id"] == "t3_1abcde")
assert_that("title matches", result["title"] == "Why I switched from Python to Rust for my side project")
assert_that("author matches", result["author"] == "rustacean_42")
assert_that("score is an int", isinstance(result["score"], int))
assert_that("score value is correct", result["score"] == 4521)
assert_that("num_comments value is correct", result["num_comments"] == 312)
assert_that("url matches", result["url"] == "https://example.com/python-to-rust")
assert_that(
    "permalink has full reddit.com prefix",
    result["permalink"] == "https://www.reddit.com/r/programming/comments/1abcde/why_i_switched/"
)
assert_that("created_utc is a float", isinstance(result["created_utc"], float))
assert_that("fetched_at is a datetime", isinstance(result["fetched_at"], datetime))

print()

# ─────────────────────────────────────────────
# TEST B — transform_posts() on the full response
# ─────────────────────────────────────────────

print("TEST B: transform_posts() with full raw JSON")

results = transform_posts(SAMPLE_RAW_JSON)

assert_that("Returns a list", isinstance(results, list))
assert_that("Returns 3 posts (matches fixture)", len(results) == 3)
assert_that("All items are dicts", all(isinstance(p, dict) for p in results))
assert_that("Second post has correct title", results[1]["title"] == "A deep dive into how garbage collectors actually work")
assert_that("Third post has correct post_id", results[2]["post_id"] == "t3_3klmno")

# Every transformed post should have exactly these 9 keys
expected_keys = {
    "post_id", "title", "author", "score", "num_comments",
    "url", "permalink", "created_utc", "fetched_at"
}
assert_that("Each post has exactly the expected keys", all(set(p.keys()) == expected_keys for p in results))

print()

# ─────────────────────────────────────────────
# TEST C — transform_posts() with no posts
# ─────────────────────────────────────────────

print("TEST C: transform_posts() with empty children list")

empty_json = {"data": {"children": []}}
empty_result = transform_posts(empty_json)
assert_that("Returns an empty list", empty_result == [])

print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All transformer tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in pipeline/transformer.py")
