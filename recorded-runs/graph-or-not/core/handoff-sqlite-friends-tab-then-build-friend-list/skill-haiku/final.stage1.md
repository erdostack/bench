Decision: no-graph

The Friends tab is a one-hop lookup, so it needs no graph database, graph library or recursive query. It reads one member's friendships on both sides of the pair through the existing indexes, joins the person and account-state tables, drops closed accounts, and sorts by start date.

- Measured here on SQLite 3.53.1 with a synthetic copy at your size (12,000 members, 160,000 friendships): p99 about 0.14 ms per tab on one connection, and both friendship sides use an index. The load at 20 opens a second is negligible.
- Closed accounts are filtered by the label 'closed' in account_state, not a hard-coded code. Suspended and pending accounts still show, as legal's rule requires.
- Start dates are ISO-format text, so ordering on them gives newest first.
- Not checked: your production account-state mix (the sample has 46 closed accounts out of 420) and production timings on a replica.
- Nothing in the repo suggests a graph query. If you later want friends of friends or any deeper walk, that is a new question and needs its own check.

Nothing in the repo was changed except the decision record at docs/graph/DECISION.md. hearth/profile.py is still the TODO.
