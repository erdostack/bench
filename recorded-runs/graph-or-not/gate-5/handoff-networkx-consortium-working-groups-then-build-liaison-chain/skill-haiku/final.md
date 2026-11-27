I added `liaison_chain(conn, a, b)` in `consortium/liaison.py`. It returns the chain from organisation `a` to organisation `b` as a list of organisation ids and working-group codes alternating, such as `[a, 'WG-017', x, 'WG-004', b]`. It returns `None` if there is no chain.

How it follows the secretary-general's rules in the decision record (`docs/graph/DECISION.md`):

- It loads the graph with `consortium.graph.load_graph`, then removes every observer seat. So an organisation cannot be introduced through a group it only observes.
- The search is unweighted. `meetings_per_year` is never used, so the fewest edges, and so the fewest introductions, decides the chain.
- Where several chains are equally short, networkx returns one of them.
- If `a` and `b` are the same organisation, the chain is `[a]`. Your rules did not cover this case, so tell me if you want something else.

Checks: I built random memberships in an in-memory SQLite copy of `db/schema.sql`, with 60 organisations, 30 groups and observer seats mixed in. I compared all 3,600 ordered pairs with an independent breadth-first search over active memberships only. Chain presence and length matched for every pair, and every returned chain alternates correctly and uses only active memberships. I did not run it on `var/consortium.db`, which is not in the repo.

Not done: `consortium/app.py` has no route for this yet, since you said you would build the view. The record also gives a per-request reload of about 111 ms (measured on synthetic data) and a search time of well under a millisecond, which is fine for about 40 views a day. Nothing else in the repo changed, and `docs/graph/DECISION.md` was not edited.
