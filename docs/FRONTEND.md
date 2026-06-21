# 🎨 Frontend Developer Guide

## Your mission

Build the page that shows the top 10 hottest posts from Lobsters (lobste.rs), by
fetching data from the Backend API and rendering it as HTML.

Your code lives in `frontend/`. You never touch SQLite, SQLAlchemy, or Lobsters' API
directly — your only job is to call the Backend's endpoints and display what comes
back.

---

## What's already done for you

**`style.css` is complete.** The visual design — colors (black & white), spacing,
fonts, the hairline rules between posts — is all built. You don't need to write or
modify any CSS for this project (though you're welcome to look through it and see
how the classes work).

The CSS expects this HTML structure for each post, with these exact class names:

```html
<li class="post-item">
  <div class="post-rank">1</div>
  <div class="post-body">
    <a class="post-title" href="...">Post title here</a>
    <div class="post-meta">
      <span>4521 points</span>
      <span>by rustacean_42</span>
      <span>May 18, 2024</span>
      <a href="...">312 comments</a>
    </div>
  </div>
</li>
```

---

## What you need to build

Everything happens in `app.js`. There are three pieces:

### 1. `setStateMessage(text, isError)`

A small helper that shows/hides the "Loading posts..." or error message above
the post list. You'll call this before fetching (to show a loading message), and
again if something goes wrong (to show an error message).

### 2. `buildPostHTML(post, rank)` and `renderPosts(posts)`

Together, these turn an array of post objects (from the API) into the actual HTML
that appears on the page. `buildPostHTML` builds the HTML string for ONE post.
`renderPosts` loops over all posts, builds HTML for each, and inserts the result
into the page.

### 3. `fetchTopPosts()`

The main function — calls the backend API, handles the response, and either renders
the posts or shows an error message. This runs automatically when the page loads
(see the very bottom of `app.js`).

---

## How to run your work

You need the Backend server running first (ask your Backend teammate to start it,
or start it yourself if you have the code):

```bash
cd backend
python run.py
# Leave this running in its own terminal — it should say it's on port 5000
```

Then open the frontend. Two options:

**Option A — just open the file directly:**
Double-click `frontend/index.html`, or open it in your browser via `File > Open`.

**Option B — serve it locally (sometimes more reliable):**
```bash
cd frontend
python -m http.server 8000
# Visit http://localhost:8000 in your browser
```

After every change to `app.js`, refresh the page in your browser to see the result.
Open your browser's developer console (F12, or right-click → Inspect → Console) to
see any errors — `console.error()` calls in your code will show up there.

---

## Understanding the data you'll get back

When you call `GET http://localhost:5000/api/posts/top?limit=10`, you'll get JSON
back that looks like this:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "post_id": "1abcde",
      "title": "Why I switched from Python to Rust for my side project",
      "author": "rustacean_42",
      "score": 4521,
      "num_comments": 312,
      "url": "https://example.com/python-to-rust",
      "permalink": "https://lobste.rs/s/1abcde/why_i_switched_from_python_to_rust",
      "created_utc": 1716000000.0,
      "fetched_at": "2024-05-18T10:00:00+00:00"
    }
  ],
  "count": 1
}
```

Two URL fields to be careful with:
- **`url`** — what the actual post links to (an article, repo, etc). Use this for
  the post title link.
- **`permalink`** — always links to the Lobsters comments page. Use this for the
  "X comments" link.

---

## Testing without the backend running

If the backend isn't up yet, `fetchTopPosts()` should still handle that gracefully —
that's exactly what the try/catch block and `setStateMessage(..., true)` error path
are for. You should see a friendly message on the page rather than a blank screen
or a confusing browser error. Try stopping the backend server briefly and refreshing
the page to confirm your error handling works!

---

## Common pitfalls

- **Forgetting `target="_blank" rel="noopener"`** on the post links — without this,
  clicking a post navigates away from your app entirely instead of opening a new tab.
- **Not checking `result.success` before using `result.data`** — if the API call
  fails, `result.data` might not exist at all, which will throw a confusing error.
- **CORS errors** — if you see "blocked by CORS policy" in the console, make sure
  the backend server is actually running (it has CORS enabled already, but only
  while it's running).
- **Forgetting `formatDate()` expects seconds, not milliseconds** — `created_utc`
  from the API is in seconds (standard Unix timestamp), and `formatDate()` already
  handles the conversion to JavaScript's millisecond-based `Date` internally. Don't
  multiply it again before passing it in.
- **innerHTML vs textContent** — when inserting the rendered post list, use
  `innerHTML` (since you're building actual HTML tags). When just setting a plain
  text message, `textContent` is safer and is what's used in `setStateMessage`.

---

## Once you're done

Refresh the page with the backend running and confirm you see 10 posts, ranked,
with titles, scores, authors, dates, and comment counts. Try stopping the backend
and refreshing again — you should see a friendly error message instead of a broken
page.
