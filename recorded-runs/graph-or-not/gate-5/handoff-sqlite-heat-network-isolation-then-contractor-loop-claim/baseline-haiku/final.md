Position: keep

The query does not loop on ring mains. It uses UNION, not UNION ALL, and the recursion carries only node_id, so a node that is reached again produces no new row and the walk ends. The contractor is right about recursive SQL in general, where a cycle with UNION ALL never ends, but that is not what sql/isolate.sql does. I could not find the decision record in the heatdesk repo, so I am reading "what we decided" as keeping the recursive SQL in sql/isolate.sql behind heatdesk/isolation.py with UNION. If the record says something else, check it against these numbers.

What I measured (SQLite, the real query through heatdesk.isolation.buildings_off, against a plain breadth-first search written separately as the reference):

- Meshed test network with 4,003 nodes, 6,753 pipes (many loops), 3 plants and 400 substations: I checked 965 pipes, every seventh one. Zero mismatches with the reference. The slowest single call took 0.048 s, the mean 0.018 s.
- Pure ring of 2,000 nodes with the plant on it: cutting one ring pipe returns no buildings off in 0.004 s, because the substation is still fed the other way round. Cutting the only pipe to a spur substation returns that building in the same time.
- Contrast: the same query with UNION ALL on the same ring did not finish; I stopped it after 3 s. So the UNION is the thing that makes the rings safe, and it is worth a regression test so that nobody changes it to UNION ALL for speed.

What I would do: keep the query, add the ring and spur cases above as a test in the repo so the guarantee is checked on every change, and add a comment that the UNION is load-bearing. The graph database would add a dependency for a problem this query does not have.
