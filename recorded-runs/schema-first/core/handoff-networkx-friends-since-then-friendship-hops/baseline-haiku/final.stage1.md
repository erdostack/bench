I added `friends(G, person_id)` in `social/friends.py`. It returns a dict mapping each friend's person id to the date the friendship started, as `YYYY-MM-DD`.

- `G` is the graph from `social.graph.load()`.
- A `knows` edge is stored once, in whichever direction the request went, so the function reads both directions.
- Friendships that have a `deletionDate` are left out, because they have ended. The export has 33 such edges. If the console should also show ended friendships, that is a one-line change, so say if you want it.
- It raises `ValueError` if no person has that id.

I checked it against `data/social.graphml`: for all 196 people, the result matches the set of current friends in an undirected view of the graph, and every date is a valid `YYYY-MM-DD` string. Example: person 10116 has 7 current friends. I did not wire it into the recommendations service, since the request was for the function.
