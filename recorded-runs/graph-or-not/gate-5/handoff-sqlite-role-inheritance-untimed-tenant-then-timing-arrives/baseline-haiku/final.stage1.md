Decision: need-more-information

The decision rule Sanne set depends on one measurement we do not have: the indexed recursive query on the enterprise tenant. Until that is timed, the evidence cannot say whether the query meets the 3 s p95 budget on SQLite. The 6 ms p95 on the 39 small tenants does not carry over, for a specific reason below.

Why the small-tenant timing does not settle it:

- `EFFECTIVE_SQL` walks inheritance as paths. Each row carries its own path string, and the cycle check only stops a walk from revisiting a role on that same path. It does not stop two different walks from reaching the same role. So the recursion produces one row per distinct path through the inheritance graph, not one row per role.
- Where inheritance is shaped like a diamond (a role inherits two parents that share ancestors), the number of paths grows exponentially with depth. I checked this with the real query on layered synthetic tenants in SQLite (a stand-in, not the real data):

  | layers | width | roles | walk rows produced | distinct permissions | time |
  |---|---|---|---|---|---|
  | 8 | 2 | 16 | 255 | 15 | 0.012 s |
  | 12 | 2 | 24 | 4,095 | 23 | 0.014 s |
  | 16 | 2 | 32 | 65,535 | 31 | 0.203 s |
  | 10 | 3 | 30 | 29,524 | 28 | 0.098 s |

  The distinct permission counts stay small while the walk rows multiply. The synthetic layers are fully connected between neighbouring layers, which is denser than most real hierarchies. Even so, the pattern is the thing to watch: the work grows with the number of paths, not the number of roles.
- The enterprise tenant has roughly 40 times the roles of the next biggest and inheritance that goes a lot deeper. Both push in the direction of that growth. Nobody has timed it, so the 6 ms number cannot be used for it.

What would decide it:

1. Time `EFFECTIVE_SQL` p95 on the enterprise tenant. The export to the test box keeps failing, so fix that, or build a copy of the tenant's role, role_inherits, role_permission and user_role rows through another route. Time the real admin-console query for the users that matter, not only one user.
2. Count the walk rows for those users, not just elapsed time. A large walk-row count with a fast time is still a risk on busier data.

What to do with each result, under Sanne's rule:

- If the current query meets 3 s p95 on the enterprise tenant, no new datastore. Stay on SQLite.
- If it misses, the rule says move role inheritance to the identity team's graph store. Before that, one SQL change is worth trying, because it is not a SQLite workaround in the sense Sanne means. Replace the path-tracking walk with a visited-set walk: `UNION` on `role_id` alone, with no path string and no `instr` check. Rows then deduplicate per role, the walk is linear in inherited edges, and the query stays recursive SQL with the existing `role_inherits_parent` index. Time it on the same enterprise copy. If it meets budget, the decision is recursive-sql. If not, the graph store applies.

Recommendation: do not stand up a new datastore yet, and do not call the decision until the enterprise tenant is timed on both the current and the visited-set query.
