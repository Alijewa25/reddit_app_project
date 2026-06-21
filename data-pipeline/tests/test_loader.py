"""
============================================================
TESTS — Pipeline Layer 3: Loader
============================================================
Run with:  python tests/test_loader.py

These tests use a SEPARATE test database file (test_reddit.db)
so they never touch your real reddit.db. The test database is
deleted and recreated each time you run this file.
============================================================
"""

import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ─────────────────────────────────────────────
# SET UP AN ISOLATED TEST DATABASE BEFORE IMPORTING THE LOADER
# ─────────────────────────────────────────────
# We override the DB_PATH that db.py uses, BEFORE pipeline.loader
# (which imports pipeline.db) gets imported. This keeps test data
# completely separate from your real reddit.db.

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "test_reddit.db")
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

import pipeline.db as db_module
db_module.DB_PATH = TEST_DB_PATH
db_module.DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_module.engine = create_engine(db_module.DATABASE_URL, echo=False)
db_module.SessionLocal = sessionmaker(bind=db_module.engine)

from pipeline.models import Base, Post
Base.metadata.create_all(bind=db_module.engine)

from pipeline.loader import load_posts

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
# SAMPLE DATA
# ─────────────────────────────────────────────

def make_post(post_id, title, score, num_comments=10):
    return {
        "post_id": post_id,
        "title": title,
        "author": "test_author",
        "score": score,
        "num_comments": num_comments,
        "url": "https://example.com/test",
        "permalink": "https://www.reddit.com/r/programming/comments/test/",
        "created_utc": 1716000000.0,
        "fetched_at": datetime.now(timezone.utc),
    }

# ─────────────────────────────────────────────
# TEST 1 — Inserting brand new posts
# ─────────────────────────────────────────────

print("TEST 1: load_posts() inserts new posts")

new_posts = [
    make_post("t3_aaa111", "First test post", 100),
    make_post("t3_bbb222", "Second test post", 200),
]
summary = load_posts(new_posts)

assert_that("Summary reports 2 inserted", summary["inserted"] == 2)
assert_that("Summary reports 0 updated", summary["updated"] == 0)
assert_that("Summary reports total of 2", summary["total"] == 2)

# Verify directly in the database
session = db_module.get_session()
all_posts = session.query(Post).all()
assert_that("Database now has 2 rows", len(all_posts) == 2)
session.close()

print()

# ─────────────────────────────────────────────
# TEST 2 — Re-loading the same post_id updates it (upsert)
# ─────────────────────────────────────────────

print("TEST 2: load_posts() updates existing posts (upsert)")

updated_posts = [
    make_post("t3_aaa111", "First test post", 999, num_comments=50),  # same post_id, new score
]
summary2 = load_posts(updated_posts)

assert_that("Summary reports 0 inserted (already existed)", summary2["inserted"] == 0)
assert_that("Summary reports 1 updated", summary2["updated"] == 1)

session = db_module.get_session()
all_posts = session.query(Post).all()
assert_that("Database STILL has only 2 rows (no duplicate)", len(all_posts) == 2)

updated_row = session.query(Post).filter_by(post_id="t3_aaa111").first()
assert_that("Score was updated to 999", updated_row.score == 999)
assert_that("num_comments was updated to 50", updated_row.num_comments == 50)
assert_that("Title stayed the same (we don't update title)", updated_row.title == "First test post")
session.close()

print()

# ─────────────────────────────────────────────
# TEST 3 — Mixed batch: some new, some existing
# ─────────────────────────────────────────────

print("TEST 3: load_posts() with a mixed batch")

mixed_posts = [
    make_post("t3_aaa111", "First test post", 1500),   # existing → update
    make_post("t3_ccc333", "Third test post", 300),    # new → insert
]
summary3 = load_posts(mixed_posts)

assert_that("Summary reports 1 inserted", summary3["inserted"] == 1)
assert_that("Summary reports 1 updated", summary3["updated"] == 1)

session = db_module.get_session()
all_posts = session.query(Post).all()
assert_that("Database now has 3 rows total", len(all_posts) == 3)
session.close()

print()

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────

print("─" * 45)
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 All loader tests passed!")
else:
    print("⚠️  Some tests failed. Complete the TODOs in pipeline/loader.py")

# Clean up the test database file
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)
