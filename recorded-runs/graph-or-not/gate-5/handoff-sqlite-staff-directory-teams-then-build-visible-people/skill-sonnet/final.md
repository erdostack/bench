I added `visible_people(conn, person_id)` to `directory/profiles.py` and replaced the TODO there. I touched no other file.

It follows `docs/graph/DECISION.md` (no-graph, plain joins on SQLite). A person is visible when they share a team with `person_id` that has at most 40 current members.
- Only current rows count (`left_at IS NULL`), both for who is in the team and for its size, so the company-wide and location teams don't make everyone visible.
- It returns distinct ids, never `person_id` itself, in no particular order.
- The cap is a constant, `MAX_SHARED_TEAM_SIZE = 40`.

I tried it on a small in-memory database built from `db/schema.sql`. It covered a team of exactly 41 being ignored, an ended membership not counting for either side, a duplicate current row for one person returning them once, and a person with no teams. I haven't timed it at the stated size. The decision record's measurement (12 ms worst case) came from a different query, so I haven't confirmed that figure for this one.

The record leaves one point open, so I made a choice. A person's own profile is not in the result, as you specified, so the page needs to allow viewing your own profile separately if that's wanted.
