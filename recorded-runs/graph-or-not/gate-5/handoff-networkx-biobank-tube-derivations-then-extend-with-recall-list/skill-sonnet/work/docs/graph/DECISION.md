# Graph decision

Decision: in-process-library

The recall list is every descendant of a recalled tube through any number of aliquots, extractions and pools, with destroyed tubes left off the list but still walked through. That is a walk of data-dependent depth along a relation between tubes. The data is 18,400 tubes and 21,900 derivation rows from a nightly export, which is small enough to hold in memory, and networkx is already in the repo for the lineage plots, so the answer is to walk it there and not adopt Neo4j.

## Workload facts

- 18,400 tubes and 21,900 derivation rows in the nightly export; chains up to 6 steps; a few recalls a month (stated by the user)
- Rule from the lab manager: the recall list holds every tube derived from the recalled one, through any number of aliquots, extractions and pools; tubes already destroyed are left off the list, but whatever was made from them before they were destroyed is still on it (stated by the user)
- 212 tube ids differ only by case or a trailing space because LIMS B exports lower case; the lab confirmed they are the same tube (stated by the user)
- Question asked: descendants of one node in a directed graph, depth depends on the data (tubetrack/graph.py builds `nx.DiGraph` from parent_id to child_id; `nx.ancestors` is already used for lineage plots)
- Edges per tube = 21,900 / 18,400 = about 1.2 derivation rows per tube (stated by the user, divided)
- Memory: networkx holds a graph of this size in tens of megabytes at most (21,900 edges even at 1 KB per edge is about 22 MB; the bytes per edge is an assumption, not measured), against one process (arithmetic from the stated counts)
- Freshness: the export is nightly, and the file is reloaded for each plot call today (README.md, tubetrack/graph.py `derivation_graph`); a recall a few times a month needs the data as of the last export (README.md)
- Load: a few recalls a month, so a few calls a month and no latency budget stated (stated by the user)
- Data in the repo is a small sample: 600 tubes (status stored 443, destroyed 109, shipped 48) and 588 derivation rows (LIMS A 411, LIMS B 177), measured with a Python count over data/tubes.csv and data/derivations.csv
- Measured on the sample: derivation rows reference 797 distinct raw ids, which collapse to 582 after stripping spaces and upper-casing; 354 rows have an id with different case or a trailing space (rows from LIMS B). Every normalized id is also in tubes.csv, which has no case or space variants.
- Measured on the sample: after normalising, the graph has 582 nodes and 588 edges, is acyclic, and its longest chain is 10 derivation steps, longer than the 6 the user stated. Highest out-degree is 6 (measured with networkx 3.7).
- tubetrack/graph.py does not normalise ids, so today's lineage plots treat a lower-case LIMS B id and its upper-case twin as two tubes and break chains between the labs (tubetrack/graph.py `add_edge(row["parent_id"], ...)`)
- Operated today: Python 3.12, networkx 3.7, two CSV files; there is no SQL database in the repo (README.md, requirements.txt)
- unknown: whether `shipped` tubes belong on the recall list; the rule only exempts destroyed tubes, so they stay on it unless the lab manager says otherwise
- unknown: whether the export can contain a derivation cycle in the full data (the sample has none)
- unknown: the status column in the full export (only `stored`, `destroyed`, `shipped` are seen in the sample)

## Options considered

- graph-database (Neo4j for "sample genealogy", Priya's proposal): rejected, because the full data is 21,900 edges, loaded nightly and queried a few times a month, so there is no size, load or freshness problem a second stateful system would solve, and it would need its own copy fed from the export.
- in-process-library (networkx, already in requirements.txt): chosen, because the edges fit in the memory of one process by a wide margin (about 22 MB at the assumed 1 KB per edge) and the nightly export is reloaded on each call in `derivation_graph`. The recall list is `nx.descendants` from the normalised id, walking through destroyed tubes and then dropping them from the result, and keeping everything else, including shipped tubes.
- recursive-sql (recursive CTE): rejected, because there is no SQL database in the repo, only two CSV files; adopting one for this would add a store with no gain over the walk in the app.
- no-graph (plain joins): rejected, because the descendants through a variable number of steps cannot be got with a fixed number of joins; chains in the sample reach 10 steps.

## What would change the decision

- Recalls running through the full 21,900 rows taking longer than a lab manager will wait (nobody has stated a limit; the lab manager sets it), measured as the load plus walk time on the full export, would point to caching the graph in the process, which stays in-process-library.
- The edge set growing by a factor of a thousand (about 20 million edges), or reads needing data fresher than the nightly export, would call for re-measuring memory per edge and could move this to graph-database or recursive-sql.
- A derivation cycle found in the full export would need a check before the walk; the lab manager decides how to flag it.
- The lab manager ruling that shipped tubes are not pulled would change which statuses are dropped from the list; the walk stays the same.
