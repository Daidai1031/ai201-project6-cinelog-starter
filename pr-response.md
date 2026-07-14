# PR Response Doc — CineLog Watchlist Feature

## AI Usage
- File summary: summuarize the main function, dependency of models.py, services/collection_service.py, and tests/test_collection.py.
e.g.  "[models.py](models.py) Summarize what this file is responsible for, what its main functions do, and what other parts of the codebase it depends on"
- Function explanation: "What does this function do? Walk me through what happens at each step, and what it returns if the film_id doesn't exist." Use this on add_to_collection() (cpmment2)
- Test structure: Give the AI the test_collection.py file and ask: "What pattern does each test follow? What do I need to provide to write a test in the same style?" (comment4)
## Comment 1 — Rename

save_to_watchlist() should follow the project's naming convention. Compare with add_to_collection() — the pattern here is verb_to_noun. Please rename to add_to_watchlist() and update all call sites.

**What I did:**
Use ctrl+shift+f found all `save_to_watchlist` in 3 places, in 2 files: `services/watchlist_service.py` for defination, `routes/watchlist/watchlist.py` for import function and call function.
Renamed `save_to_watchlist()` to `add_to_watchlist()` to follow the project's `verb_to_noun` naming convention. I also updated the import and route call site to use the new function name.

**How I verified:**
Searched the repository to confirm that no references to `save_to_watchlist` remained. I also ran `pytest -q` and confirmed that all tests passed.


## Comment 2 — Deduplication

What happens if a user calls this with a film that's already on their watchlist? The current implementation would add a duplicate entry. Please handle this case.

**What I did:**

**How I verified:**

## Comment 3 — Missing test

Please add a test for the case where film_id doesn't exist in the database. Look at the existing tests in test_collection.py — the pattern is there.

**What I did:**

**How I verified:**

## Comment 4 — Default visibility

I notice watchlists default to public=True. We don't have a documented decision on default visibility for user lists. Before I can approve this, I need you to add a note to your PR description explaining your reasoning. I want to make sure we're being intentional here, not just inheriting a default.

**My position:**
**Reasoning:**
**Tradeoff acknowledged:**

## Comment 5 — Sort order

I'd prefer watchlists to default to "date added" order rather than alphabetical. Most users want to see what they added recently. I'm open to discussion if you see it differently — but let's make a decision and document it.

**My position:**
**Reasoning:**
**Engagement with reviewer's point:**

## Comment 6 — Rebase

A refactor merged to main that changed film IDs from integers to UUIDs. Your watchlist code still references integer IDs. Please rebase on main and update accordingly.

**What conflicted:**
**How I resolved it:**
**How I verified no conflict remains:**

## PR Description