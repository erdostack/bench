Decision: no-graph

The visibility rule does not need a graph database, a graph library or a recursive query. A profile is visible when the viewer and the target share a current team with at most 40 current members. That is one hop through the membership table, which the existing indexes already serve: about 8 ms per check on SQLite at the stated scale, or roughly 0.4 seconds of database time per minute at 50 views a minute.

- The company-wide team (8,900 people) is excluded by the size limit, not by any special case. Its size is the expensive part of each check, because the count reads its membership entries every time.
- Ended memberships have to be excluded both when deciding who is in a team and when counting its size. Each `team_member` condition in the check needs `left_at IS NULL`, and the team-size count must carry the same filter.
- Test the query against the DPO's examples on a copy of the real database before it ships, since the 6 MB file is not in the repo and my timings come from synthetic data.

The full evidence, the options considered and what would change the decision are in `docs/graph/DECISION.md` in the working directory. Nothing else in the repo was changed.
