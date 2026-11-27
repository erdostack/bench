Decision: no-graph

Skip Neo4j and skip a graph library. "Who can see whom" here is a single hop, not a traversal. The viewer sees the person if they are both current members of some team that has 40 or fewer current members. That is one self-join on `team_member` plus a count. No path-following is involved. At 41,000 rows in a 6 MB SQLite file, with the indexes on `person_id` and `team_id` that already exist, it needs nothing else. Recursive SQL isn't needed either, because nothing recurses.

What I changed (`directory/profiles.py`):
- `can_view(conn, viewer_id, person_id)` returns True for your own profile. Otherwise it returns True when a team contains both people as current members (`left_at IS NULL`) and that team has at most 40 current members.
- `visible_profile(conn, viewer_id, person_id)` returns the profile or `None`.
- Ended memberships are excluded from who is in the team and from its size, as the DPO rule says.
- A person who rejoined has several rows for the same team, so the size is a count of distinct people. Otherwise rejoiners would make a 40-person team look bigger than 40.
- The size count stops at 41, so the 8,900-person company team is ruled out without scanning it all.
- The limit is the constant `MAX_SHARED_TEAM_SIZE = 40`.
- `profile()` itself is unchanged, and I haven't wired `visible_profile` into any caller. There is no web layer in this repo, so you'll need to call it from wherever profile pages are served.

Checks, on synthetic data of the same shape (9,200 people, 1,350 teams, about 40,000 rows):
- Two people who share only the company team: not visible.
- A team with 41 current members: not visible. After one of them leaves, it has 40 and becomes visible.
- A team with 40 current members and 5 ended ones: visible. A team with 40 distinct current members but 45 rows because of rejoiners: also visible.
- Viewer or target with an ended membership: not visible.
- A rejoiner: visible.
- Your own profile: visible.
- Speed: 2,000 checks took 0.3 s, about 0.15 ms each. The expected 50 views a minute is far below what this can handle.

Open points:
- The rule says "colleagues you share a team with" and I read it as every `kind` of team (project, location and company included) being subject to the 40-person cap. The cap is what stops the location and company teams making everyone visible. If the DPO wants some kinds excluded outright, that is a one-line filter on `team.kind`.
- A team that is exactly 40 counts, and 41 does not, per "at most 40".
- The check is only as good as the data. The nightly HR sync must set `left_at` promptly, or people who have left will still count.
- I have not run this against the production database.
