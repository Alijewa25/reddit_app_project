"""
============================================================
PIPELINE ENTRY POINT — run_pipeline.py
============================================================
Role: Data Engineer

This is the script you run to actually pull fresh data from
Lobsters and store it in the database.

It calls the three pipeline layers IN ORDER:
    1. fetcher.fetch_top_posts_raw()    → raw Lobsters JSON
    2. transformer.transform_posts()    → clean list of dicts
    3. loader.load_posts()              → saved into lobsters.db

Run it from the data-pipeline/ folder with:
    python run_pipeline.py

You should re-run this periodically (e.g. once a day) to keep
scores and comment counts up to date. For this student project,
running it manually whenever you want fresh data is enough —
in a real production system this would be a scheduled cron job.
============================================================
"""

from pipeline.db import init_db
from pipeline.fetcher import fetch_top_posts_raw
from pipeline.transformer import transform_posts
from pipeline.loader import load_posts


def run():
    print("=== Lobsters Top Posts Pipeline ===\n")

    print("Step 0: Ensuring database tables exist...")
    init_db()
    print("  ✅ Database ready.\n")

    print("Step 1: Fetching raw data from lobste.rs (hottest)...")
    raw_json = fetch_top_posts_raw(limit=10)
    print(f"  ✅ Fetched {len(raw_json)} raw stories.\n")

    print("Step 2: Transforming raw data into our schema...")
    clean_posts = transform_posts(raw_json, limit=10)
    print(f"  ✅ Transformed {len(clean_posts)} posts.\n")

    print("Step 3: Loading posts into the database...")
    summary = load_posts(clean_posts)
    print(f"  ✅ Inserted: {summary['inserted']}, Updated: {summary['updated']}, "
          f"Total processed: {summary['total']}\n")

    print("=== Pipeline run complete! ===")


if __name__ == "__main__":
    run()