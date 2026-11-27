Decision: recursive-sql

Nothing to change. The where-used walks 400,000 BOM lines at 180 ms p95, 600 times a day, well under the 800 ms
line you and Ines agreed, and it already handles the PLM loops. The contractor's graph database would be a second
store for a walk that works. I wrote the rule down in docs/graph/DECISION.md (800 ms, then networkx in the ECO
service, 350 MB / 20 ms in Ana's prototype), since it isn't anywhere in the repo.
