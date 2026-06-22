# 🔧 Backend Developer Guide

## Your mission

Build a Flask API that reads posts out of `lobsters.db` and serves them as JSON, so the
frontend has something to fetch and display.

Your code lives in `backend/`. You never write a database query directly in a Flask
route, and you never call Lobsters' API — that's the Data Engineer's job. You only
read what's already in the database.

---

## Your three layers

```
repository.py  →  service.py  →  routes.py
(raw database     (business        (HTTP layer —
 queries)          logic, formats   Flask routes)
                   for the API)
```

### 1. `app/models.py` — the schema (coordinate with your Data Engineer)

This MUST match `data-pipeline/pipeline/models.py` exactly — both files describe the
same `posts` table in the same `lobsters.db` file. Get this from your Data Engineer
teammate as soon as they've finished it, and keep both files in sync if it ever changes.

This file also has one extra method beyond the pipeline's version: `to_dict()`. This
converts a `Post` database object into a plain dictionary — which is what we need
before we can turn it into JSON.

### 2. `app/repository.py` — talk to the database

This is the ONLY file in the backend that writes `session.query(...)` calls. Its job
is to answer questions like "give me the top N posts" or "find this one post" — it
returns `Post` objects (or lists of them) straight from the database.

This layer doesn't know anything about HTTP, JSON, or Flask. It would look exactly
the same if this backend were a CLI tool instead of a web API.

### 3. `app/service.py` — business logic

Sits between the raw database layer and the HTTP layer. Its main jobs:
- Convert `Post` objects into plain dicts (using `.to_dict()`) so they're JSON-ready
- Apply small business rules, like making sure nobody can request more than 50 posts
  at once (this is called "clamping" a value to a safe range)
- Wrap results in a consistent `{"success": ..., "data": ...}` shape

### 4. `app/routes.py` — the actual API endpoints

This is where Flask comes in. Each function here handles one HTTP endpoint: reads
query parameters or URL segments from the request, calls the service layer, and
returns a JSON response with the right status code.

Notice the pattern: a route function should be SHORT. If you find yourself writing
a database query or a complicated calculation inside a route function, that logic
probably belongs in `service.py` or `repository.py` instead.

---

## How to run your work

```bash
cd backend
pip install -r requirements.txt

# Make sure the Data Engineer has already run the pipeline once,
# so lobsters.db actually has data in it!

# Start the server:
python run.py
# Now visit http://localhost:5000/api/health in your browser
```

Test each layer individually as you build it:

```bash
python tests/test_repository.py   # uses a temporary seeded test database
python tests/test_service.py       # mocks the repository — pure logic test
python tests/test_routes.py        # uses Flask's test client, mocks the service
```

**Recommended build order:** `models.py` (with your Data Engineer) → `db.py` →
`repository.py` → `service.py` → `routes.py`. Each layer's tests only depend on the
layer(s) below it being done, so you can verify your progress as you go.

---

## Try it without waiting for the Data Engineer

Notice that `tests/test_repository.py` seeds its OWN small test database with fake
posts — it doesn't depend on the real pipeline having run yet. This means you can
start building and testing your repository layer in parallel with the Data Engineer's
work, as long as you've both agreed on the schema first.

---

## Common pitfalls

- **Forgetting to close sessions** → Every `get_session()` call should eventually be
  followed by `session.close()`. Leaving sessions open can cause subtle bugs.
- **Returning `Post` objects directly as JSON** → Flask's `jsonify()` can't serialize
  SQLAlchemy objects directly. Always convert with `.to_dict()` first (in the service
  layer, not the route).
- **Datetime serialization errors** → `fetched_at` is a Python `datetime` object,
  which isn't valid JSON. The `.to_dict()` method should convert it with
  `.isoformat()`.
- **CORS errors in the browser console** → The frontend runs on a different port than
  the backend, so without CORS enabled, the browser will block the request. This is
  already set up for you via `flask_cors.CORS(app)` in `routes.py` — just don't
  remove it!
- **Wrong status codes** → A "not found" result should return HTTP 404, not 200.
  Check the TODO comments in `routes.py` carefully for which status code each case needs.

---

## Once you're done

Run all three test files and confirm everything passes, then start the server with
`python run.py` and leave it running. Visit these URLs in your browser to sanity-check
manually:

- http://localhost:5000/api/health
- http://localhost:5000/api/posts/top
- http://localhost:5000/api/stats

That's your hand-off point to the Frontend team — they'll be calling these exact URLs.