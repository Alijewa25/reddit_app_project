"""
============================================================
PIPELINE LAYER 1 — FETCHER
============================================================
Role: Data Engineer

Responsibility: Talk to Reddit's public JSON endpoint and return
the RAW response data. This layer does NOT clean, validate, or
reshape anything — it just fetches and hands back what Reddit gave us.

Why a separate layer for this?
  - If Reddit changes their API, only this file needs to change.
  - We can test the rest of the pipeline with fake fetched data,
    without needing the internet.

IMPORTANT — Reddit requires a descriptive User-Agent header.
Requests without one (or with a generic one like "python-requests")
will be blocked or heavily rate-limited. This is documented in
Reddit's own API rules: always identify your app, platform, and
a contact username.
============================================================
"""

import requests

# Reddit blocks default/generic User-Agents. Always send something
# descriptive that identifies your app.
USER_AGENT = "python:reddit-top-posts-student-project:v1.0 (by /u/Huseyn1211)"

REDDIT_TOP_URL = "https://old.reddit.com/r/programming/top.json"


def fetch_top_posts_raw(time_filter: str = "month", limit: int = 10) -> dict:
    """
    Fetches the raw top-posts JSON from Reddit for r/programming.

    Args:
        time_filter (str): Reddit's time window — "month" gives us
                            "top posts this month". Other valid values
                            Reddit accepts: "day", "week", "year", "all".
        limit (int): How many posts to request (Reddit allows up to 100).

    Returns:
        dict: The raw parsed JSON response from Reddit.

    Raises:
        requests.HTTPError: If Reddit responds with an error status code.

    TODO:
        - Build a `params` dict: {"t": time_filter, "limit": limit}
        - Build a `headers` dict: {"User-Agent": USER_AGENT}
        - Call requests.get(REDDIT_TOP_URL, params=params, headers=headers, timeout=10)
        - Call response.raise_for_status() to raise an error on bad status codes
        - Return response.json()

    HINT: Reddit's JSON shape looks like this (simplified):
        {
          "data": {
            "children": [
              { "data": { "id": "...", "title": "...", "author": "...", ... } },
              { "data": { ... } },
              ...
            ]
          }
        }
        You don't need to unpack this here — that's Layer 2's job.
        Just return the whole raw dict.
    """
    params = {"t": time_filter, "limit": limit}
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(REDDIT_TOP_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()