Decision: in-process-library

The recall list is a walk over every descendant of the recalled tube, at any depth, that stops at nothing but the end of the chain. The whole derivation graph is small, and networkx is already in the repo for the lineage plots, so load it in the application and walk it. A graph server (Priya's Neo4j idea) costs more than a few recalls a month justify.

Things to fix before the recall tool is built:

- The ids must be normalised on load (strip spaces, upper-case). `tubetrack/graph.py` uses the raw ids today, so 176 of the 582 tube ids in the repo's data get a different recall list. For BB-0002 the raw graph gives 5 tubes and the normalised graph gives 28.
- The walk must pass through destroyed tubes and leave them off the returned list. Stopping at destroyed tubes would lose tubes for 90 of the 582 sources in the repo's data.
- Nothing in the repo was run against the lab's systems, and nothing was changed except the new file docs/graph/DECISION.md.

Numbers that do not agree, and need checking with the lab:

1. You gave 18,400 tubes and 21,900 derivation rows. The repo's data has 600 tubes and 588 derivation rows. Is `data/` a sample, or is the nightly export different?
2. You gave chains up to 6 steps. The longest chain in the repo's data is 10 links.
3. You gave 212 ids that differ only by case or a trailing space. The repo's data has 215 such spellings.

Questions for the lab manager:

1. Is the recalled source tube itself on the list?
2. Do the derivation rows carry a date? The rule says children made before a tube was destroyed stay on the list, and the export has no dates to check this with.
3. How stale may the list be? The export is nightly, so a tube destroyed today will not be known to the list until tomorrow.
4. Shipped tubes are not destroyed, so under the rule they stay on the list. Confirm that is intended.
