Decision: in-process-library

This is connected components over 140 lines and about 2,300 line-station rows: lines are linked when they share a station. It needs graph logic, but only a few lines of it, once a month. A graph database or recursive SQL would add more than the problem needs.

What I did: I implemented `line_groups(conn)` in `netmap/groups.py`.
- It reads `line` and `line_station` into memory and merges lines that share a station with a small union-find.
- It returns `{line_id: family}`. Families are numbered from 1 in order of their lowest line_id, so the output is the same on every run. A line with no stations gets its own family.
- I used plain Python and not networkx. networkx is installed on this machine, but this repo doesn't declare any dependency, so I didn't add one. If you'd rather use `nx.connected_components`, it is a small swap.

Check: I ran it on a toy network of 5 lines. Lines 1, 2 and 3 are chained through shared stations, line 4 is separate and line 5 has no stations. It gave families 1, 1, 1, 2 and 3. I didn't run it against the real `var/rail.db`, which isn't in the repo, and I didn't add a test file.

Why not the others: a graph database means a new system to run and sync for a monthly job over about 2,300 rows. Recursive SQL would work, but it is harder to read and to test than this. This isn't a good first use for a graph database.

One point to confirm: I read "connect" as "share a station". If the map should also count interchanges such as walking links between nearby stations, the schema has no data for that.
