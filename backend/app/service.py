"""
============================================================
BACKEND LAYER 2 — SERVICE
============================================================
Role: Backend Developer

Responsibility: Sits between the Repository (raw DB queries) and
the API routes (HTTP handling). Converts ORM objects into plain
dicts, and is the place to add business rules later (e.g. "only
show posts with score > 0", "limit max 50 per request", etc).

This layer does NOT know about Flask, requests, or HTTP status codes.
It does NOT write raw SQL queries — that's the Repository's job.
============================================================
"""

from app import repository


def get_top_posts_for_api(limit: int = 10) -> dict:
    """
    Gets the top posts and formats them for the API response.

    Args:
        limit (int): How many posts to return.
                     Should be clamped between 1 and 50 for safety.

    Returns:
        dict: {"success": True, "data": [list of post dicts], "count": int}

    TODO:
        1. Clamp limit to a safe range:
               if limit < 1: limit = 1
               if limit > 50: limit = 50
        2. Call repository.get_top_posts(limit) to get Post ORM objects
        3. Convert each Post object to a dict using its .to_dict() method:
               posts_data = [post.to_dict() for post in posts]
        4. Return {"success": True, "data": posts_data, "count": len(posts_data)}
    """
    if limit < 1:
        limit = 1
    if limit > 50:
        limit = 50

    posts = repository.get_top_posts(limit)
    posts_data = [post.to_dict() for post in posts]
    
    return {"success": True, "data": posts_data, "count": len(posts_data)}


def get_single_post_for_api(post_id: str) -> dict:
    """
    Gets one post by id and formats it for the API response.

    Args:
        post_id (str): The Reddit post_id to look up.

    Returns:
        dict: On success: {"success": True, "data": post_dict}
              On failure: {"success": False, "error": "Post not found."}

    TODO:
        - Call repository.get_post_by_id(post_id)
        - If the result is None:
              return {"success": False, "error": "Post not found."}
        - Otherwise:
              return {"success": True, "data": post.to_dict()}
    """
    post = repository.get_post_by_id(post_id)
    if post is None:
        return {"success": False, "error": "Post not found."}
    
    return {"success": True, "data": post.to_dict()}


def get_stats_for_api() -> dict:
    """
    Gets simple stats about the dataset for a health/stats endpoint.

    Returns:
        dict: {"success": True, "data": {"total_posts": int}}

    TODO:
        - Call repository.count_posts()
        - Return {"success": True, "data": {"total_posts": count}}
    """
    count = repository.count_posts()
    return {"success": True, "data": {"total_posts": count}}