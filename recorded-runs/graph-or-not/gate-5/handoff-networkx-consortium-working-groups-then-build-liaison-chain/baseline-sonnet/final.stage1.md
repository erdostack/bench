Decision: in-process-library

Use networkx, which the app already uses. I would not move the memberships into Neo4j. The data is small (4,200 organisations, 380 groups, 27,000 memberships). The export lands nightly, and the view will be used about 40 times a day. `consortium/graph.py` already loads the export into a networkx graph every time the app needs one. A breadth-first search over a graph that size takes milliseconds. Neo4j would mean a second database, a nightly load into it, and an operations burden for the secretariat's 40 lookups a day. I did not pick recursive SQL: shortest path over a bipartite graph is awkward there, and the graph module already exists.

**What I added**
- `liaison_chain(g, from_org, to_org)` in `consortium/graph.py`.
  - It follows the secretary-general's rules. Observer seats are filtered out of the search, so an org can't introduce or be introduced through a group it only observes. Chair and member seats count.
  - "Shortest" means fewest introductions, which is plain breadth-first search. The attendance `weight` is not passed to the search, so it plays no part. The code says so in its docstring, so nobody adds `weight="weight"` later.
  - The result alternates org, group, org, group and so on. If two chains are equally short, one of them is returned.
  - It returns `None` if there is no chain, and raises `KeyError` if either id isn't an organisation.
- `GET /chain/<from_org>/<to_org>` in `consortium/app.py`, replacing the TODO.
  - If a chain exists, it returns `found: true`, the number of introductions, and each step with its id, kind and name.
  - If there is none, it returns `found: false` with the message "No chain of introductions between these organisations."
  - An unknown organisation id gets a 404.
  - Asking for a chain from an org to itself returns just that org, with zero introductions.

**Things to know**
- `groups_of` and the existing `/orgs/<id>/groups` view still include observer seats. That is existing behaviour and I left it alone. If the secretariat wants observers hidden there too, that's a separate decision.
- The view reloads the whole graph on each request (the existing `_graph()` pattern). At 40 uses a day that is fine, and I kept it. If traffic grows, load it once per nightly refresh instead.
- The route returns JSON, like the existing view. There is no HTML template in the repo, so if the secretariat wants a page, that is a small follow-up.

**Checks**
There is no `var/consortium.db` in the repo, so I tested with a small in-memory database through Flask's test client. It covered: a chain of two introductions; an observer-seat shortcut that was correctly ignored, including a case where a high attendance weight did not change the result; an org that is only an observer; an isolated org; the same org on both ends; and an unknown id. All gave the expected results. I haven't run it on the real export, and I didn't add a test file.

**When to revisit**
Only if the questions get heavier, such as weighted or constrained paths over much larger data, or many queries per second. That isn't the case here.
