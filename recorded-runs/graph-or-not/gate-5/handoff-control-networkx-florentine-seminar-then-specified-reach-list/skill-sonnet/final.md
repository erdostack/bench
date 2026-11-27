I added `families_within(conn, family, k)` to `seminar/reach.py`. It returns the sorted list of the other families reachable from `family` through at most `k` marriage ties. A tie counts in either direction, and the family itself is never in the list. The list is empty when nothing is reachable, including for `k = 0` and for the Pucci, who have no ties.

I followed the recorded decision in `docs/graph/DECISION.md`, which chose recursive SQL on the existing SQLite file. The query takes both directions of each tie and uses `UNION`, so each family is visited once. Depth is limited by your `k`, not the record's fixed 3. I didn't add Neo4j or any other dependency, and I left `DECISION.md` and `seminar/app.py` unchanged.

I checked it against `networkx` on an in-memory copy of the database, built as `seminar/load.py` builds it. I compared all 16 families plus the Pucci for `k` from 0 to 5, and there were 0 mismatches. For example, the Medici at `k = 1` give Acciaiuoli, Albizzi, Barbadori, Ridolfi, Salviati and Tornabuoni. I didn't run it against `var/seminar.db`, since that file isn't built in the repo.

I haven't wired it into the "reach" panel in `app.py` (the TODO there).
