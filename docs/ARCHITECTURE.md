# 🏗️ Architecture Overview

**Read this together as a team before splitting up to work on your own parts.**

---

## The big picture

Three independent pieces, talking to each other through well-defined boundaries:

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   reddit.com/r/programming/top.json                                │
│            │                                                        │
│            │  HTTP GET (no auth needed, just a User-Agent header)   │
│            ▼                                                        │
│   ┌──────────────────────┐                                          │
│   │   DATA PIPELINE        │  Runs on a schedule (or manually)      │
│   │   (Python script)       │  Lives in: data-pipeline/              │
│   └──────────┬───────────┘                                          │
│              │  writes rows                                         │
│              ▼                                                       │
│   ┌──────────────────────┐                                          │
│   │   reddit.db              │  A single SQLite file                │
│   │   (SQLite database)       │  Shared by pipeline + backend        │
│   └──────────┬───────────┘                                          │
│              │  reads rows                                          │
│              ▼                                                       │
│   ┌──────────────────────┐                                          │
│   │   BACKEND API            │  Runs continuously                   │
│   │   (Flask server)          │  Lives in: backend/                  │
│   │   localhost:5000           │                                     │
│   └──────────┬───────────┘                                          │
│              │  HTTP GET / JSON responses                           │
│              ▼                                                       │
│   ┌──────────────────────┐                                          │
│   │   FRONTEND                │  Runs in the browser                │
│   │   (HTML/CSS/JS)            │  Lives in: frontend/                 │
│   └──────────────────────┘                                          │
│                                                                      │
└────────────────────────────────────────────────────────────────────┘
```

---

## Why split it this way?

**The pipeline and the API never run at the same moment doing the same thing.**
The pipeline's job is to occasionally go fetch fresh data and store it. The API's job
is to constantly be ready to serve whatever is currently stored. They don't need to
talk to each other directly — they communicate **through the database**, like two
people leaving notes in a shared notebook instead of needing to be in the same room
at the same time.

This is a very common real-world pattern:
- A pipeline (or "batch job", or "ETL job") runs separately, on its own schedule.
- An API serves a fast, read-only view of whatever the pipeline most recently produced.
- A frontend never touches the database or the pipeline directly — only the API.

---

## The shared contract: the database schema

Both the Data Engineer's pipeline and the Backend Developer's API need to agree on
**exactly** what a "post" looks like in the database. This is defined in `models.py`
(once in each folder — they must match).

| Column | Type | Meaning |
|---|---|---|
| `id` | Integer | Internal database row id (auto-generated) |
| `post_id` | String | Reddit's own unique id, e.g. `"t3_1abcde"` |
| `title` | String | Post title |
| `author` | String | Reddit username of the poster |
| `score` | Integer | Upvotes |
| `num_comments` | Integer | Comment count |
| `url` | String | What the post links to |
| `permalink` | String | Link to the comments page on reddit.com |
| `created_utc` | Float | When the post was made on Reddit (Unix timestamp) |
| `fetched_at` | DateTime | When OUR pipeline pulled this row in |

**If this schema needs to change, the Data Engineer and Backend Developer must agree
and update BOTH copies of `models.py` together.** This is exactly the kind of
coordination real engineering teams do constantly — it's why having a clear, written
schema matters so much.

---

## The shared contract: the API response shape

The Backend Developer and Frontend Developer need to agree on what JSON the API sends
back. This project uses a consistent shape across all endpoints:

**Success:**
```json
{
  "success": true,
  "data": [ ... ],
  "count": 10
}
```

**Failure:**
```json
{
  "success": false,
  "error": "Post not found."
}
```

The frontend should always check `result.success` before trying to use `result.data`.

---

## Endpoints the Frontend will call

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/posts/top?limit=10` | Top N posts by score |
| GET | `/api/posts/<post_id>` | One specific post |
| GET | `/api/stats` | Total post count (for debugging/health) |
| GET | `/api/health` | Is the server alive? |

---

## What happens if a layer is broken?

This is the benefit of layered architecture — you can isolate problems:

- **Frontend shows "Could not reach the API"** → Backend server isn't running, or
  the wrong port/URL is being used. Check `python run.py` is running in `backend/`.
- **Backend returns an empty list `[]`** → The database has no data yet. Check the
  Data Engineer has run `python run_pipeline.py` at least once.
- **Pipeline fails with a network error** → Check your internet connection, and check
  the `User-Agent` header is being sent (Reddit blocks requests without one).
- **Pipeline runs but backend can't find any posts** → Check both `models.py` files
  actually point at the same `reddit.db` path, and that the schema matches.

Each team can test their own layer in isolation using the test files provided —
you don't need the other two layers running to verify your own code works.
