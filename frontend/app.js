/**
 * ============================================================
 * FRONTEND LOGIC — app.js
 * ============================================================
 * Role: Frontend Developer
 *
 * Responsibility: Fetch the top posts from the Backend API and
 * render them into the page.
 *
 * This file talks to ONE place: the backend API at API_BASE_URL.
 * It does NOT know about SQLite, SQLAlchemy, or Reddit's JSON
 * format — by the time data reaches this file, the backend has
 * already cleaned and formatted it.
 *
 * Flow:
 *   1. Page loads → fetchTopPosts() runs automatically
 *   2. fetchTopPosts() calls the API → gets JSON back
 *   3. renderPosts() turns that JSON into HTML on the page
 *   4. If something goes wrong, showError() displays a message
 * ============================================================
 */

const API_BASE_URL = "http://localhost:5000";

// ─────────────────────────────────────────────
// DOM REFERENCES
// ─────────────────────────────────────────────

const postListEl = document.getElementById("post-list");
const stateMessageEl = document.getElementById("state-message");

// ─────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────

/**
 * Formats a Unix timestamp (seconds) into a readable date string.
 * Example: 1716000000 → "May 18, 2024"
 *
 * This one is implemented for you as an example of working with
 * the `created_utc` field that comes back from the API.
 *
 * @param {number} unixSeconds
 * @returns {string}
 */
function formatDate(unixSeconds) {
  const date = new Date(unixSeconds * 1000);
  return date.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
}

/**
 * Shows a message in the state-message area (loading / error / empty).
 * Pass isError = true to apply the red error styling.
 *
 * @param {string} text
 * @param {boolean} isError
 */
function setStateMessage(text, isError = false) {
  // TODO:
  //   - Set stateMessageEl.textContent = text
  //   - If isError is true, add the "error" CSS class to stateMessageEl
  //     (stateMessageEl.classList.add("error"))
  //   - If isError is false, make sure the "error" class is removed
  //     (stateMessageEl.classList.remove("error"))
  //   - If text is empty (""), hide the element entirely:
  //     stateMessageEl.style.display = "none"
  //     Otherwise make sure it's visible: stateMessageEl.style.display = ""

    stateMessageEL.textConetnt = text;
  if(isError === true){
    sateMessageEL.classList.add("error");
  }else if(isError === false){
    stateMessageEL.classlist.remove("error");
  }else if(text === ""){
    stateMessageEL.style.display = "none";
  }else if(text !== ""){
    stateMessageEL.style.display = "";
  }
}

// ─────────────────────────────────────────────
// RENDERING
// ─────────────────────────────────────────────

/**
 * Builds the HTML for a SINGLE post and returns it as a string.
 *
 * Each post object from the API looks like this:
 *   {
 *     "id": 1,
 *     "post_id": "t3_1abcde",
 *     "title": "Why I switched from Python to Rust",
 *     "author": "rustacean_42",
 *     "score": 4521,
 *     "num_comments": 312,
 *     "url": "https://example.com/python-to-rust",
 *     "permalink": "https://www.reddit.com/r/programming/comments/...",
 *     "created_utc": 1716000000.0,
 *     "fetched_at": "2024-05-18T10:00:00+00:00"
 *   }
 *
 * @param {Object} post - A single post object from the API.
 * @param {number} rank - The post's position in the list (1, 2, 3...).
 * @returns {string} HTML string for one <li class="post-item">...</li>
 *
 * TODO:
 * 
 *   Build and return an HTML string using the post's fields and
 *   the CSS classes already defined in style.css. It should look
 *   like this (use template literals — backticks):
 *
 *   `
 *     <li class="post-item">
 *       <div class="post-rank">${rank}</div>
 *       <div class="post-body">
 *         <a class="post-title" href="${post.url}" target="_blank" rel="noopener">
 *           ${post.title}
 *         </a>
 *         <div class="post-meta">
 *           <span>${post.score} points</span>
 *           <span>by ${post.author}</span>
 *           <span>${formatDate(post.created_utc)}</span>
 *           <a href="${post.permalink}" target="_blank" rel="noopener">
 *             ${post.num_comments} comments
 *           </a>
 *         </div>
 *       </div>
 *     </li>
 *   `
 *
 *   Notes:
 *     - post.url is where the post itself links to (could be an
 *       article, repo, etc).
 *     - post.permalink is always the Reddit comments page —
 *       use that one for the "comments" link.
 *     - Use formatDate(post.created_utc) for a readable date.
 */
<li class="post-item">
  <div class="post-rank">${rank}</div>
  <div class="post-body">
    <a class="post-title" href="${post.url}" target="_blank" rel="noopener">
      ${post.title}
    </a>
    <div class="post-meta">
      <span>${post.score} points</span>
      <span>by ${post.author}</span>
      <span>${formatDate(post.created_utc)}</span>
      <a href="${post.permalink}" target="_blank" rel="noopener">
        $post.num_comments comments
      </a>
    </div>
  </div>
</li>
function buildPostHTML(post, rank) {
}

/**
 * Renders the full list of posts into the page.
 *
 * @param {Array} posts - Array of post objects from the API.
 *
 * TODO:
 *   - If posts is empty (posts.length === 0):
 *       Call setStateMessage("No posts found. Has the pipeline been run yet?")
 *       and return early (don't continue to build the list).
 *   - Otherwise:
 *       Call setStateMessage("") to hide the loading/error message.
 *       Build the full HTML by mapping over `posts` and calling
 *       buildPostHTML(post, index + 1) for each one (rank starts at 1,
 *       not 0 — that's why we use index + 1).
 *       Join the array of HTML strings together with "" and set it as
 *       postListEl.innerHTML.
 *
 *   HINT:
 *     const html = posts.map((post, index) => buildPostHTML(post, index + 1)).join("");
 *     postListEl.innerHTML = html;
 */
if(posts.length === 0){
  setStateMessage("No posts found. Has the pipeline been run yet?");
  return;
}else if(posts.length > 0){
  setStateMessage("");
  const html = posts.map((post, index) => buildPostHTML(post, index + 1)).join("");
  postListEl.innerHTML = html;
}
function renderPosts(posts) {
}

// ─────────────────────────────────────────────
// DATA FETCHING
// ─────────────────────────────────────────────

/**
 * Fetches the top posts from the backend API and renders them.
 * Handles loading and error states along the way.
 *
 * TODO:
 *   1. Call setStateMessage("Loading posts...") before the fetch starts.
 *
 *   2. Use fetch() to call: `${API_BASE_URL}/api/posts/top?limit=10`
 *      This returns a Promise, so use async/await or .then() chains.
 *
 *   3. Check if the response is ok (response.ok). If NOT ok, throw an
 *      Error so it's caught by your catch block, e.g.:
 *          throw new Error(`Server responded with status ${response.status}`)
 *
 *   4. Parse the JSON body: const result = await response.json()
 *
 *   5. Check result.success:
 *      - If true: call renderPosts(result.data)
 *      - If false: call setStateMessage(result.error || "Something went wrong.", true)
 *
 *   6. Wrap steps 2-5 in a try/catch block. In the catch block:
 *      call setStateMessage(
 *        "Could not reach the API. Is the backend server running on port 5000?",
 *        true
 *      )
 *      (Also console.error(error) so you can debug in the browser console.)
 *
 *   EXAMPLE SHAPE (fill in the real logic):
 *
 *   async function fetchTopPosts() {
 *     setStateMessage("Loading posts...");
 *     try {
 *       const response = await fetch(`${API_BASE_URL}/api/posts/top?limit=10`);
 *       if (!response.ok) {
 *         throw new Error(`Server responded with status ${response.status}`);
 *       }
 *       const result = await response.json();
 *       if (result.success) {
 *         renderPosts(result.data);
 *       } else {
 *         setStateMessage(result.error || "Something went wrong.", true);
 *       }
 *     } catch (error) {
 *       console.error(error);
 *       setStateMessage("Could not reach the API. Is the backend server running on port 5000?", true);
 *     }
 *   }
 */
setStateMessage("Loading posts...");
try{
  const response = await fetch(`${API_BASE_URL}/api/posts/top?limit=10`);
  if(!response.ok){
    throw new Error(`Server responded with status ${response.status}`);
  }
  const result = await response.json();
  if(result.success){
    renderPosts(result.data);
  }else{
    setStateMessage(result.error || "Sommething went wrong ", true);

  }
  }catch(error){
    console.error(error);
    setStateMessage("Cloud not reach the API. Is the backend server running on port 5000?", true);
  }
async function fetchTopPosts() {
}

// ─────────────────────────────────────────────
// RUN ON PAGE LOAD
// ─────────────────────────────────────────────

fetchTopPosts();
