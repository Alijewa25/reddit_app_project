"""
============================================================
PIPELINE LAYER 2 — TRANSFORMER
============================================================
Role: Data Engineer

Responsibility: Take the RAW Reddit JSON (from fetcher.py) and turn
it into a clean list of plain Python dicts that match our database
schema exactly (see pipeline/models.py).

This layer does NOT touch the network and does NOT touch the database.
It is pure data transformation — easy to test, easy to reason about.

Why a separate layer for this?
  - Reddit's raw JSON has dozens of fields we don't need, with messy
    nesting. This layer is the ONE place that knows how to translate
    "Reddit's shape" into "our shape".
  - If our database schema changes, only this file (and models.py)
    need to change — not the fetcher.
============================================================
"""

from datetime import datetime, timezone


def transform_post(raw_post_data: dict) -> dict:
    """
    Transforms a SINGLE raw Reddit post object into our schema shape.

    Args:
        raw_post_data (dict): The "data" object from one Reddit post,
            e.g. raw_json["data"]["children"][0]["data"]

    Returns:
        dict: A dict with exactly these keys, matching models.Post:
            {
                "post_id": str,        <- raw_post_data["id"], prefix with "t3_"
                "title": str,          <- raw_post_data["title"]
                "author": str,         <- raw_post_data["author"]
                "score": int,          <- raw_post_data["score"]
                "num_comments": int,   <- raw_post_data["num_comments"]
                "url": str,            <- raw_post_data["url"]
                "permalink": str,      <- "https://www.reddit.com" + raw_post_data["permalink"]
                "created_utc": float,  <- raw_post_data["created_utc"]
                "fetched_at": datetime <- datetime.now(timezone.utc)
            }

    TODO:
        - Build and return the dict described above.
        - For post_id, prepend "t3_" to raw_post_data["id"]
          (this is Reddit's own convention for marking it as a "link" type).
        - For permalink, prepend "https://www.reddit.com" to
          raw_post_data["permalink"] (Reddit gives you a relative path).
        - For fetched_at, use datetime.now(timezone.utc) to record
          the moment OUR pipeline processed this post.
    """
    pass  # Remove this line when you implement the function


def transform_posts(raw_json: dict) -> list:
    """
    Transforms the FULL raw Reddit response into a list of clean dicts.

    Args:
        raw_json (dict): The full raw dict returned by fetcher.fetch_top_posts_raw()

    Returns:
        list[dict]: A list of transformed post dicts (see transform_post above).
                     Returns an empty list if there are no posts.

    TODO:
        - Navigate to the list of posts: raw_json["data"]["children"]
        - This is a list where each item looks like: { "data": {...} }
        - For each item, call transform_post(item["data"])
        - Collect the results into a list and return it.

        HINT: A list comprehension works well here:
            return [transform_post(child["data"]) for child in raw_json["data"]["children"]]
    """
    pass  # Remove this line when you implement the function
