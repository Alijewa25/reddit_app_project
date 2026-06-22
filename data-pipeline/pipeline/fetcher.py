"""
============================================================
PIPELINE LAYER 1 — FETCHER
============================================================
Role: Data Engineer

Responsibility: Talk to Lobsters' public JSON endpoint and return
the RAW response data. This layer does NOT clean, validate, or
reshape anything — it just fetches and hands back what Lobsters gave us.

Why a separate layer for this?
  - If Lobsters changes their API, only this file needs to change.
  - We can test the rest of the pipeline with fake fetched data,
    without needing the internet.

ABOUT THE DATA SOURCE — lobste.rs:
Lobsters (lobste.rs) is a programming-focused link aggregator. It has
simple, public, unauthenticated JSON endpoints — no API key, no login,
no OAuth needed:

    https://lobste.rs/hottest.json   <- "hottest" front page stories
    https://lobste.rs/newest.json    <- newest submitted stories

There is no "top this month" time-window parameter — Lobsters'
"hottest" endpoint is its own ranking algorithm (a mix of score and
recency), and that's what we use here as our "top posts" source.
It's good practice to still send a descriptive User-Agent identifying
your app, even though it isn't strictly required.
============================================================
"""

import requests

# Good practice: always identify your app with a descriptive User-Agent,
# even for APIs that don't strictly require one.
USER_AGENT = "python:lobsters-top-posts-student-project:v1.0 (by Huseyn1211)"

LOBSTERS_HOTTEST_URL = "https://lobste.rs/hottest.json"


def fetch_top_posts_raw(limit: int = 10) -> list:
    """
    Fetches the raw "hottest" stories JSON from Lobsters.

    Args:
        limit (int): How many stories we ultimately want to keep.
                     Lobsters' hottest.json always returns its full
                     front-page list (usually 25) in one response —
                     there's no `limit` query param to ask for fewer.
                     We still accept `limit` here so the function
                     signature matches how the rest of the pipeline
                     calls it; trimming to `limit` happens in Layer 2
                     (the transformer), not here.

    Returns:
        list: The raw parsed JSON response from Lobsters — a LIST of
              story dicts (there's no wrapping "data" object; Lobsters
              just returns a flat JSON array).

    Raises:
        requests.HTTPError: If Lobsters responds with an error status code.

    TODO:
        - Build a `headers` dict: {"User-Agent": USER_AGENT}
        - Call requests.get(LOBSTERS_HOTTEST_URL, headers=headers, timeout=10)
        - Call response.raise_for_status() to raise an error on bad status codes
        - Return response.json()

    HINT: Lobsters' JSON shape looks like this (simplified, one story):
        [
          {
            "short_id": "xacdsk",
            "title": "Secret EU law threatens Internet security",
            "url": "https://last-chance-for-eidas.org/",
            "score": 32,
            "comment_count": 16,
            "comments_url": "https://lobste.rs/s/xacdsk/secret_eu_law...",
            "created_at": "2023-11-02T03:47:05.000-05:00",
            "submitter_user": { "username": "galadran", ... },
            "tags": ["browsers", "cryptography"]
          },
          { ... },
          ...
        ]
        It's a flat list — no nested wrapper object to dig through.
        You don't need to unpack anything here — that's Layer 2's job.
        Just return the whole raw list.
    """
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(LOBSTERS_HOTTEST_URL, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()
