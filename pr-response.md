# PR Response Doc — CineLog Watchlist Feature

## AI Usage
<!-- Fill in at the end. Document at least one specific use of AI during this project.
     Examples: codebase orientation, understanding add_to_collection(), verifying
     conventional commit format, stress-testing your Comment 4 / Comment 5 arguments.
     If you used AI on Comment 4 or 5, describe what you asked and how your final
     reasoning differs from what the AI returned. If you didn't use AI, say so. -->

---

## Comment 1 — Rename `save_to_watchlist` → `add_to_watchlist`

**What I did:**
Renamed `save_to_watchlist()` to `add_to_watchlist()` in `services/watchlist_service.py`
to follow the project's `verb_to_noun` naming convention (matching `add_to_collection()`).
Updated both call sites in `routes/watchlist/watchlist.py` — the import and the function call.

**How I verified:**
Ran `git grep -n save_to_watchlist`, which returned no results, confirming every reference
was updated. `pytest tests/` still passed.

---

## Comment 2 — Deduplication

**What I did:**
Added deduplication to `add_to_watchlist()`, mirroring the pattern in `add_to_collection()`:
after confirming the film exists, query for an existing `WatchlistEntry` with the same
`user_id` and `film_id`, and raise a new `AlreadyInWatchlistError` if one is found instead
of inserting a duplicate. Wired the route to return HTTP 409 for that error (and 404 for a
nonexistent film, which the route previously did not handle).

**How I verified:**
Compared against `add_to_collection()`'s `filter_by(...).first()` check to match the existing
pattern. Added a duplicate-entry test (see Comment 3) that asserts the second add raises and
that only one entry exists in the database.

---

## Comment 3 — Missing test

**What I did:**
Created `tests/test_watchlist.py`, modeled on `tests/test_collection.py` (same in-memory app
fixture, same user/film fixtures). Added the required test for a nonexistent `film_id`
(`test_add_to_watchlist_nonexistent_film_raises`), plus a happy-path test and a duplicate test
to satisfy CONTRIBUTING.md's requirement of happy-path / duplicate / nonexistent coverage for
a new service function.

**How I verified:**
Ran `pytest tests/ -v` — all tests pass.

---

## Comment 4 — Default visibility

> Reviewer (@dev-lead): "I notice watchlists default to `public=True`. We don't have a
> documented decision on default visibility for user lists. Before I can approve this, I need
> you to add a note to your PR description explaining your reasoning. I want to make sure we're
> being intentional here, not just inheriting a default."

**My position:**
<!-- State clearly: should the default be public or private? -->

**Reasoning:**
<!-- Ground this in CineLog specifically — it's a community film-tracking app. What user
     behavior are you optimizing for? Who benefits from the default you chose, and how does it
     fit how CineLog users actually use watchlists? A one-liner won't earn credit. -->

**Tradeoff acknowledged:**
<!-- Name the real downside of your choice. What does the OTHER option get right that yours
     gives up? (e.g., privacy expectations vs. discovery/social value) -->

---

## Comment 5 — Sort order

> Reviewer (@dev-lead): "I'd prefer watchlists to default to 'date added' order rather than
> alphabetical. Most users want to see what they added recently. I'm open to discussion if you
> see it differently — but let's make a decision and document it."

**My position:**
<!-- Keep alphabetical (Film.title.asc()), switch to date-added (date_added.desc()), or propose
     a third option. Note whether you changed the code and, if so, to what. -->

**Reasoning:**
<!-- Argue for YOUR choice. If you agree with the reviewer, still explain WHY date-added fits
     CineLog rather than just deferring. If you disagree, make the case. -->

**Engagement with reviewer's point:**
<!-- The reviewer gave a specific rationale ("most users want to see what they added recently").
     Address that claim directly — agree, refine, or push back with your own reasoning. -->

---

## Comment 6 — Rebase

**What conflicted:**
<!-- Fill in after rebasing on origin/main. The main branch migrated film IDs from integer to
     UUID; your watchlist code (models.py WatchlistEntry.film_id, docstrings) still used int. -->

**How I resolved it:**
<!-- Describe updating WatchlistEntry.film_id from db.Integer to db.String(36) with the UUID
     foreign key, and any docstring/type updates. -->

**How I verified no conflict remains:**
<!-- git status clean, pytest tests/ passes, git log --oneline shows no merge commits. -->

---

## git log --oneline (final history)

<!-- Paste a screenshot of `git log --oneline` on feature/watchlist here after the Milestone 4
     interactive rebase. It should show at least 4 conventional commits and no merge commits. -->

---

## PR Description

**What the watchlist feature does:**
<!-- 2–3 plain-language sentences: users can save films they want to watch later, view their
     watchlist, with duplicate protection and visibility control. -->

**Design decisions:**
<!-- Explicitly name BOTH: (1) default visibility (Comment 4) and (2) sort order (Comment 5),
     with one-line summaries of what you chose. -->

**How to manually test the feature:**
<!-- Step-by-step with curl. Example shape:
     1. Start the app: python app.py
     2. (Seed a user and film / note their IDs)
     3. Add to watchlist:
        curl -X POST http://127.0.0.1:5000/watchlist/<user_id>/add \
          -H "Content-Type: application/json" -d '{"film_id": "<film_id>"}'
     4. View the watchlist: curl http://127.0.0.1:5000/watchlist/<user_id>
     5. Add the same film again -> expect 409
     6. Add a nonexistent film -> expect 404 -->
