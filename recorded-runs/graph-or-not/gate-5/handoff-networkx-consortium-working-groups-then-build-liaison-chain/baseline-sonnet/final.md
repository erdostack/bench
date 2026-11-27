`liaison_chain(conn, a, b)` is now in `consortium/liaison.py`. It loads the graph with `consortium.graph.load_graph(conn)` and then calls the existing `liaison_chain` in `consortium/graph.py`. I didn't write a second version of the chain logic, so the rules can't drift apart.

- **Chain format:** it returns a list from `a` to `b` with organisation ids and working-group codes alternating, for example `[1, 'WG-1', 2, 'WG-2', 3]`. If `a` and `b` are the same organisation it returns `[a]`.
- **Shortest chain:** shortest means fewest introductions. Attendance (`meetings_per_year`) is ignored. If several chains are equally short, any one of them is returned.
- **Observer seats:** these don't count. Nobody is introduced through a group they only observe.
- **No chain:** it returns `None`.
- **Bad ids:** it raises `KeyError` if `a` or `b` isn't an organisation id. A working-group code or an id that doesn't exist both raise it. `/chain/<from>/<to>` in `app.py` already turns that into a 404.

I checked it by hand on a small in-memory database built from `db/schema.sql`. The cases were a multi-hop chain, a chain that would only work through an observer seat (it returned `None`), an organisation with no memberships, the same organisation twice, and a working-group code passed as an id. There is no `var/consortium.db` or test suite in the repo, so I haven't run it on real data and didn't add tests.

`consortium/graph.py` and `consortium/app.py` are unchanged. The view is yours.
