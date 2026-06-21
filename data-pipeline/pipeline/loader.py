"""
============================================================
PIPELINE LAYER 3 — LOADER
============================================================
Role: Data Engineer

Responsibility: Take the CLEAN list of post dicts (from transformer.py)
and write them into the SQLite database using SQLAlchemy.

This layer does NOT know about Reddit's JSON format and does NOT
do any network calls. It only knows how to save/update rows.

Why a separate layer for this?
  - The transform step doesn't need to know HOW data is stored.
  - We can swap SQLite for PostgreSQL later by only touching db.py
    and this file — fetcher.py and transformer.py stay untouched.

UPSERT LOGIC:
  Posts can be fetched more than once (e.g. running the pipeline daily).
  If a post_id already exists in the database, UPDATE its score and
  num_comments (since those change over time) instead of inserting
  a duplicate row.
============================================================
"""

from pipeline.models import Post
from pipeline.db import get_session


def load_posts(posts: list) -> dict:
    """
    Saves a list of transformed post dicts into the database.
    Uses upsert logic: update existing posts, insert new ones.

    Args:
        posts (list[dict]): Clean post dicts from transformer.transform_posts()

    Returns:
        dict: Summary of what happened, e.g.
              {"inserted": 7, "updated": 3, "total": 10}

    TODO:
        1. Get a database session: session = get_session()
        2. Initialize counters: inserted = 0, updated = 0
        3. For each post dict in posts:
             a. Query for an existing row with the same post_id:
                  existing = session.query(Post).filter_by(post_id=post["post_id"]).first()
             b. If existing is found:
                  - Update existing.score = post["score"]
                  - Update existing.num_comments = post["num_comments"]
                  - Increment updated += 1
             c. If NOT found:
                  - Create a new Post object using the dict's values:
                      new_post = Post(
                          post_id=post["post_id"],
                          title=post["title"],
                          author=post["author"],
                          score=post["score"],
                          num_comments=post["num_comments"],
                          url=post["url"],
                          permalink=post["permalink"],
                          created_utc=post["created_utc"],
                          fetched_at=post["fetched_at"],
                      )
                  - Add it to the session: session.add(new_post)
                  - Increment inserted += 1
        4. Commit the session: session.commit()
        5. Close the session: session.close()
        6. Return {"inserted": inserted, "updated": updated, "total": len(posts)}
    """
    session = get_session()
    inserted = 0
    updated = 0

    for post in posts:
        existing = session.query(Post).filter_by(post_id=post["post_id"]).first()

        if existing:
            existing.score = post["score"]
            existing.num_comments = post["num_comments"]
            updated += 1
        else:
            new_post = Post(
                          post_id=post["post_id"],
                          title=post["title"],
                          author=post["author"],
                          score=post["score"],
                          num_comments=post["num_comments"],
                          url=post["url"],
                          permalink=post["permalink"],
                          created_utc=post["created_utc"],
                          fetched_at=post["fetched_at"],
                      )
            session.add(new_post)

            inserted +=1
        
    session.commit()
    session.close()

    return {
        "inserted": inserted,
        "updated": updated,
        "total": len(posts)
    }
