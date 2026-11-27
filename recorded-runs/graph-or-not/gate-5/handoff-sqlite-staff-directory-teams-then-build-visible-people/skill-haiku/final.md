I added `visible_people(conn, person_id)` to `directory/profiles.py`. It returns the ids of the people whose profile `person_id` can see, in no particular order, without `person_id` itself.

A person is visible when they share a current team with `person_id`, and that team has at most 40 current members. Ended memberships count for neither: a person whose stint in the team has ended is not visible, and an ended member does not add to the team's size. The 40 is in `VISIBLE_TEAM_MAX_MEMBERS`, labelled as the DPO sign-off.

It is one join on `team_member` with a per-team count, following the recorded no-graph decision. The decision record is unchanged, and no condition in it is met.

Checked on an in-memory copy of `db/schema.sql`: a team with exactly 40 current members, including the viewer, shows the other 39; a team of 41 is excluded; an ended member is neither shown nor counted; a rejoined person uses only the current stint; and the viewer's own ended stint gives nothing. I did not run it on the real 6 MB database, which is not in the repo.

Things to know before you wire it in:
- `profile()` still returns any person. I left its TODO in place, now pointing at `visible_people()`, since the page is yours to wire up.
- The rule as stated covers only a shared team. The record notes that the DPO may mean it to reach further; the function follows the stated rule only.
- The per-check cost was measured on synthetic data at about 8 ms. A page that checks many people at once would multiply that.

Nothing else in the repository was changed.
