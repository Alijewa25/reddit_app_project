"""
============================================================
BACKEND ENTRY POINT — run.py
============================================================
Role: Backend Developer

Run this file to start the Flask API server:
    python run.py

The server will start on http://localhost:5000

Available endpoints once everything is implemented:
    GET /api/health           → check the server is alive
    GET /api/posts/top        → top 10 posts by score
    GET /api/posts/top?limit=5 → top 5 posts by score
    GET /api/posts/<post_id>  → a single post by id
    GET /api/stats            → total post count

NOTE: This requires reddit.db to already exist with data in it!
Make sure the Data Engineer's pipeline has been run at least once:
    cd ../data-pipeline
    python run_pipeline.py
============================================================
"""

from app.routes import app

if __name__ == "__main__":
    app.run(debug=True, port=5000)
