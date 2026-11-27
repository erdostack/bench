Decision: in-process-library

Build the recall list in memory with networkx, which the repo already uses for the lineage plots. No Neo4j.

Why:

- **It is a graph question, but a small, fixed one.** "Everything derived from this tube" is the descendants of one node in the derivation graph. At 18,400 tubes and 21,900 derivation rows with chains of up to 6 steps, the whole graph loads in well under a second, and a recall is a few times a month. Nothing here needs a database server, an index or a query language.
- **A graph database would be a second system for a few lookups a month.** It would need syncing from the nightly export and someone to run it. The lab has no pattern-matching or multi-hop exploration need that the descendants walk doesn't cover. Priya's "sample genealogy" idea may have value later, but it would need its own case.
- **Recursive SQL isn't available.** The data is two CSV exports, not a database. You would have to load them into SQL first, and that is more machinery than the networkx loader that already exists.

I implemented the TODO in `tubetrack/tools.py` as `recall_list(source_tube_id)`. It follows the lab manager's rule:

- It collects all descendants of the recalled tube, then drops tubes whose status is `destroyed`. The order matters: filtering during the walk would lose what was made from a destroyed tube, and the rule says that stays on the list.
- Every tube id is normalized (`strip()` and upper case) when the derivations and statuses are read, so the case and trailing-space variants from LIMS B count as the same tube, as the lab confirmed. I did not change `tubetrack/graph.py`, so the lineage plots still see those variants as separate nodes. That is a related bug you probably want fixed, by normalizing in `derivation_graph()` as well.
- The recalled tube itself is not in the result, and an unknown tube returns an empty list. Tell me if the lab wants the source tube listed as well.

I tried it on the sample data in `data/` (about 600 tubes, smaller than the production numbers you gave) and it returned plausible lists, including through lower-case rows. I haven't added tests or checked the 212 variants against production data. Two follow-ups are worth doing: a unit test where a destroyed tube sits mid-chain, and a check that every tube id in `derivations.csv` also appears in `tubes.csv`, since a missing status is currently treated as not destroyed and so stays on the list.
