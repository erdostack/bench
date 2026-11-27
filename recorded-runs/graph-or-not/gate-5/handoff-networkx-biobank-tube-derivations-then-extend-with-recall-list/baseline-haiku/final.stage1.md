Decision: in-process-library

Build the recall list with networkx, which the repo already uses for the lineage plots. Load the normalized derivation graph once, take every descendant of the recalled tube, and then drop destroyed tubes from the output. Do not stop the walk at destroyed tubes.

Why this option:
- The problem is a transitive walk (all descendants of one tube). networkx.descendants does it directly and handles any depth, so the "chains up to 6 steps" limit does not need to be coded in.
- The data is small. The sample in the repo has 600 tubes and 588 derivation rows. Even the full nightly export (18,400 tubes, 21,900 rows) fits easily in memory. A few recalls a month do not justify a second store.
- Neo4j would add a server, an import job and a second source of truth for a query that takes milliseconds in memory. "Sample genealogy" can be answered from the same CSVs.
- Recursive SQL would also work, but the lab's data arrives as CSV files, not as a database, and the lineage code already depends on networkx. Adding SQL would mean a new loading step with no gain.

Rules to build in:
- Destroyed tubes: exclude them from the list, but keep walking through them. Their children (made before destruction) stay on the list. Use the traversal result and filter on status afterwards, not a pruned walk.
- Identifiers: normalize every id with strip() and upper() before building the graph, on both the tube list and the derivation rows. The current lineage code (tubetrack/graph.py) does not do this. Checked on the repo data: the derivation file has 797 distinct raw id strings, which collapse to 582 tubes after normalization. Without normalization, descendants are silently missed. The count is 215 collapsed strings, not the 212 reported; the lab should confirm which ids were meant.
- Scope of the list: the rule as written covers derived tubes. It does not say whether the recalled source tube is itself on the pull list. Confirm this with the lab manager before the tool is used.
- Cycles: the normalized graph in the repo is a DAG, but the walk should not assume one. networkx.descendants is safe either way.

Facts from the repo data that differ from the brief:
- The longest chain in the repo data is 10 derivation steps, not 6. Check the full export before relying on a depth limit.
- The repo data is a sample (600 tubes), so timings and counts above are not for the full biobank.

Nothing was changed in the repository, and the TODO in tubetrack/tools.py was not implemented, since the request was a decision.
