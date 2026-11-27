# Graph decision

Decision: no-graph

Rhea proposes Neo4j because "who can see whom is a graph", but the privacy rule the DPO signed off is one hop: a viewer sees a profile when the two people share a team that has at most 40 current members. That is a self-join through the membership table, filtered by a per-team count, and it is answered in about 8 ms per check on SQLite at the stated scale. The finding it turns on is that no traversal exists, so the question has no graph answer to give.

## Workload facts

- People: 9,200 (stated by the user)
- Teams: 1,350, including one company-wide team of 8,900 people and office-location teams (stated by the user; the company team size is stated, the location team count is not)
- Membership rows: 41,000, of which about 6,000 are ended (left_at set), so about 35,000 current (stated by the user; 6,000 / 41,000 = 14.6% ended)
- Visibility rule, word for word from the DPO sign-off as given by the user: a shared team counts only if it has at most 40 current members; a membership that has ended does not count, neither for who is in the team nor for its size (stated by the user)
- Load: about 50 profile views a minute on a busy morning (stated by the user)
- Database: about 6 MB, one SQLite file (stated by the user; `README.md` says `var/directory.db`, which is gitignored, so the file is not in the repo)
- Query shape: viewer and target share a current team, and that team has at most 40 current members; one link table, one hop, no recursion (`directory/profiles.py` TODO; the rule above)
- Current code: no visibility check exists yet; `profile()` returns any person, and `current_teams()` and `members()` already filter `left_at IS NULL` (`directory/profiles.py`, `directory/teams.py`)
- Schema: `team_member(team_id, person_id, joined_at, left_at)` with indexes `team_member_person` and `team_member_team` (`db/schema.sql`)
- Measured, synthetic (generator in scratch, not the real data; same stated counts: 9,200 people, 1,350 teams, 41,000 rows, 6,000 ended, company team 8,900 current): the SQLite file came to 2.58 MB with short names, so it is not the 6 MB figure; the check below is a count, not a prediction of the real file (measured)
- Measured, one check = the visibility query as written with a correlated count (1,000 random pairs, first run; 300 pairs, second run): 8.5 ms and 8.1 ms per check. Plan: index search on `team_member_person` for the viewer, a correlated count per shared team through `team_member_team`, and an index search on the target's team membership (measured with `EXPLAIN QUERY PLAN`)
- Correctness cross-check: 400 random pairs compared with a brute-force check over the raw rows gave 0 disagreements for the correlated form and for a form that precomputes the small teams first (measured)
- Arithmetic: 50 views a minute x 8.1 ms per check = about 0.4 s of database time per minute, about 0.7% of one core (derived from the two measurements above; one check per view assumed, a profile page showing several people would multiply this)
- Arithmetic: the company team's current count of 8,900 is the expensive part of each check, since the correlated count reads that team's index entries each time (derived from the plan and the 8,900 count; 8.1 ms is consistent with that scan)
- unknown: real team-size distribution beyond the stated company team; the location-team count; whether a profile page checks many targets at once (a directory list would multiply the per-check cost); the real database file and its page size; whether the DPO rule is meant to reach beyond one shared team, which the stated rule does not say

## Options considered

- graph-database (a dedicated graph store, Neo4j as proposed by Rhea): rejected, because the rule needs one hop through the membership table with a size filter, which the existing indexes serve in about 8 ms per check; a second database adds sync with the nightly HR sync and the team owners' edits, and nothing in the rule is a traversal that SQL cannot express
- in-process-library (the edges loaded into memory): rejected, because no traversal runs that needs a loaded graph, and a reload would have to track membership changes made in the UI; the cost of the check is already within budget at 50 views a minute
- recursive-sql (recursive queries on the database already run): rejected for now, because the rule has no depth beyond one shared team, so no recursive query is needed; it would become the answer only if the rule itself extends to a fixed second hop, which is a self-join, not a recursion
- no-graph (plain joins, no traversal): chosen, because each visibility check is a lookup plus a join that crosses `team_member` once for the viewer and once for the target, with a per-team count, and no query follows a relation between people for more than one step; the 8 ms check at 50 views a minute meets the need as it stands

## What would change the decision

- A rule extended to a fixed second hop (colleagues of colleagues) would move this to recursive-sql, written as a self-join
- A rule extended to a walk of unbounded or data-dependent depth (transitive visibility through chains of teams) would move this to in-process-library if the membership data fits in memory and a reload meets the freshness the DPO sets, and to graph-database only if it is online, too large for a copy per process, and measured failing in SQL at that depth; the DPO sets those limits, not the repo
- A measured per-check time, from the real database file, over the latency budget the product owner sets for profile pages, or a profile page that checks a long list of targets at once, would first call for a per-team current-count column or a cached set of small teams, which is a remedy inside no-graph and not a change of option
- Trial before any spend: run the visibility query against a copy of the real 6 MB database, time one check and one full directory list, and confirm the 40-member rule and the ended-membership rule against the DPO's examples
