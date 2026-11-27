# Graph decision

Decision: in-process-library

A recall needs every tube derived from the recalled one through any number of steps, leaving out tubes already destroyed while still walking through them. That is a descendants walk over a small derivation graph (about 18,400 tubes and 21,900 derivation rows, stated by the user), and networkx is already in the repo for the lineage plots, so the graph is loaded and walked in the application for the few recalls a month. The finding it turns on is size and frequency: the walk is small and rare, which is the in-process case, and not the case a graph server is for. Separately, `tubetrack/graph.py` builds the graph from raw ids, so 176 of the 582 tube ids in the repo's data get a different recall list today; the ids must be normalised on load.

## Workload facts

- 18,400 tubes and 21,900 derivation rows in the nightly export (stated by the user). The repo's `data/` holds 600 tubes (`data/tubes.csv`) and 588 derivation rows (`data/derivations.csv`), measured here. The stated counts and the repo data disagree; which is current is unknown.
- Chains up to 6 steps (stated by the user). The longest chain in the repo's data is 10 links (measured here, normalised graph, a directed acyclic graph). The two disagree; which is right is unknown.
- Recalls: a few a month (stated by the user). Consent withdrawals are included in the same rule (stated by the user).
- Ids: 212 tube ids differ only by case or a trailing space, because LIMS B exports lower case, and the lab confirmed they are the same tube (stated by the user). Measured here: 797 raw id spellings in the derivations collapse to 582 canonical ids (215 spellings), 177 of the 588 derivation rows contain a non-canonical id, and `tubes.csv` has none. The canonical form is upper case with no spaces, as in `tubes.csv`.
- Current code: `derivation_graph()` in `tubetrack/graph.py` uses the raw ids, so the same tube appears as several nodes. Measured here: on the raw graph, the recall-style walk gives a different list for 176 of the 582 sources; for `BB-0002` it gives 5 tubes against 28 on the normalised graph.
- Destroyed tubes: 109 of 600 tubes are destroyed; 60 destroyed tubes have children (`data/tubes.csv`, measured here). Stopping the walk at destroyed tubes would lose tubes for 90 of the 582 sources (measured here), so the walk must pass through them.
- Largest recall list in the repo's data: 41 tubes; median 1; mean 3.1 (measured here, normalised graph, all 582 sources). This scales with the stated size, not measured at 18,400.
- Derivation rows and the tube export carry no dates, so the rule "made before they were destroyed" cannot be checked from these files (`data/derivations.csv`, `data/tubes.csv`). Unknown.
- Whether the recalled source tube is itself on the list is not stated (unknown). Shipped tubes are not destroyed, so under the rule as stated they stay on the list (derived from the rule).
- Freshness: the export is nightly (`README.md`). A tube destroyed after the export still appears on a recall list until the next export. Acceptable lag is not stated (unknown).
- Stack: Python 3.12 and networkx 3.7 (`requirements.txt`); `networkx` already loads the derivations for the lineage plots (`tubetrack/graph.py`).
- Existing SQL database for the biobank: none in this repo. The data arrives as CSV files from the two lab systems (`README.md`). Whether either lab system keeps a SQL database that a recursive query could use is unknown.
- Neo4j for "sample genealogy" was proposed by Priya (stated by the user); no Neo4j version or trial is recorded here.
- unknown: the true size of the nightly export; the true longest chain; whether the source tube is itself on the recall list; whether derivations carry a creation date; the acceptable freshness lag for a recall; whether a SQL database exists for the derivations.

## Options considered

- graph-database (Neo4j, as Priya proposed): rejected, because the traversal is a descendants walk over about 21,900 edges, run for a few recalls a month, with no concurrent online load or set too large for a copy per process (stated figures). A second stateful server, a nightly feed that can drift from the export, and a new query language cost more than the problem warrants.
- in-process-library (networkx, already in `requirements.txt` and used by `tubetrack/graph.py`): chosen. The whole derivation graph is small by the stated and measured counts, the walk is a standard descendants call, and the library is already a dependency. Required changes, described and not applied: normalise every id on load (strip and upper-case), traverse through destroyed tubes, and exclude destroyed tubes from the returned list.
- recursive-sql (recursive queries on an existing SQL database): passed over. The derivations are CSV files in this repo, and no SQL database is evidenced here, so the rung's precondition (an operated SQL database) is not shown to hold.
- no-graph (plain joins): rejected, because the rule asks for every tube at any depth below the source, which is a walk of unbounded depth.

## What would change the decision

- The nightly export is confirmed at the stated 18,400 tubes and 21,900 derivation rows, and the lab needs recall lists that are current within minutes rather than a night: then a live feed into a SQL or graph store is worth costing, and the owner of the freshness requirement is the lab manager.
- The lab systems keep the derivations in a SQL database that is already operated: then recursive-sql becomes the candidate, and its plan would be checked on that database before it is chosen.
- A consent or recall workflow must answer many lineage queries per minute across the biobank (online concurrency, not a few recalls a month): that is the point to test a graph database against the real query mix.
- Derivation rows carry creation dates and a tube's destroyed date is stored: then the "made before destroyed" clause can be checked in the walk, rather than assumed.
