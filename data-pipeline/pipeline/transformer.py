"""
============================================================
PIPELINE LAYER 2 — TRANSFORMER
============================================================
Role: Data Engineer

Responsibility: Take the RAW Lobsters JSON (from fetcher.py) and turn
it into a clean list of plain Python dicts that match our database
schema exactly (see pipeline/models.py).

This layer does NOT touch the network and does NOT touch the database.
It is pure data transformation — easy to test, easy to reason about.
============================================================
"""

from datetime import datetime, timezone


def transform_post(raw_post_data: dict) -> dict:
    """
    Transforms a SINGLE raw Lobsters story object into our schema shape.
    """
    parsed = datetime.fromisoformat(raw_post_data["created_at"])
    created_utc = parsed.timestamp()

    submitter = raw_post_data.get("submitter_user")
    if isinstance(submitter, dict):
        author_name = submitter.get("username", "unknown")
    else:
        author_name = str(submitter) if submitter else "unknown"

    return {
        "post_id": raw_post_data["short_id"],
        "title": raw_post_data["title"],
        "author": author_name,
        "score": raw_post_data["score"],
        "num_comments": raw_post_data["comment_count"],
        "url": raw_post_data["url"],
        "permalink": raw_post_data["comments_url"],  
        "created_utc": created_utc,
        "fetched_at": datetime.now(timezone.utc)  
    }


def transform_posts(raw_json: list, limit: int = 10) -> list:
    """
    Transforms the FULL raw Lobsters response into a list of clean dicts.
    """
    
    if not raw_json:
        return []
    
    return [transform_post(post) for post in raw_json[:limit]]