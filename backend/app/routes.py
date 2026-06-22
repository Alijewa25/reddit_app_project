"""
============================================================
BACKEND LAYER 3 — API ROUTES (Flask)
============================================================
Role: Backend Developer

Responsibility: Defines the HTTP endpoints the frontend will call.
This is the ONLY layer that knows about HTTP — request objects,
query parameters, status codes, JSON responses, and CORS.

It does NOT contain database queries (that's repository.py) and
does NOT contain business logic decisions (that's service.py).
Its job is simple: receive an HTTP request → call the service →
return an HTTP response.
============================================================
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from app import service

app = Flask(__name__)
CORS(app)  # Allows the frontend (running on a different port) to call this API


@app.route("/api/posts/top", methods=["GET"])
def get_top_posts():
    """
    GET /api/posts/top?limit=10

    Returns the top N posts ordered by score, descending.
    Query parameter `limit` is optional, defaults to 10.

    Expected JSON response:
        { "success": true, "data": [...], "count": 10 }

    TODO:
        - Read the `limit` query parameter:
              limit = request.args.get("limit", default=10, type=int)
        - Call service.get_top_posts_for_api(limit)
        - Return it as JSON: return jsonify(result)
          (Flask's jsonify automatically sets the right content type
          and status code 200 for a successful dict response)
    """
    limit = request.args.get("limit", default=10, type=int)
    result = service.get_top_posts_for_api(limit)
    return jsonify(result)


@app.route("/api/posts/<string:post_id>", methods=["GET"])
def get_post(post_id):
    """
    GET /api/posts/<post_id>

    Returns a single post by its Reddit post_id.

    Expected JSON response on success (200):
        { "success": true, "data": {...} }
    Expected JSON response on failure (404):
        { "success": false, "error": "Post not found." }

    TODO:
        - Call service.get_single_post_for_api(post_id)
        - If result["success"] is False:
              return jsonify(result), 404
        - Otherwise:
              return jsonify(result), 200
    """
    result = service.get_single_post_for_api(post_id)
    
    if result["success"] is False:
        return jsonify(result), 404
        
    return jsonify(result), 200


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """
    GET /api/stats

    Returns simple stats about the stored data — useful to confirm
    the pipeline has actually run and data exists.

    Expected JSON response:
        { "success": true, "data": { "total_posts": 10 } }

    TODO:
        - Call service.get_stats_for_api()
        - Return it as JSON: return jsonify(result)
    """
    result = service.get_stats_for_api()
    return jsonify(result)


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    GET /api/health

    Simple endpoint to confirm the server is running.
    This one is already implemented for you as an example —
    notice the pattern: receive request → return JSON response.
    """
    return jsonify({"success": True, "message": "API is running."}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
