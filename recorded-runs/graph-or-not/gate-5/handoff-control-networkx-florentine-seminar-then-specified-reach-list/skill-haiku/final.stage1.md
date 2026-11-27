Decision: recursive-sql

Build the reach panel as a recursive query on the SQLite file the app already reads. The data is 16 families and 20 marriage ties, and the walk is fixed at three steps, so the work is at most about 320 row checks per step (arithmetic). A recursive query matched networkx's distances for all 16 families (checked here in memory). Neo4j is not needed for the panel; teaching it would be a separate goal, not a workload need.

Figures: the Pucci has no ties and reaches 0 families at every depth. Medici reaches 6, 11 and 14 families at one, two and three marriages. "Reach" is taken as cumulative counts of other families within k marriages, which the instructor should confirm. Not timed: the query speed on the seminar machine. Nothing in the repo was changed except the new file docs/graph/DECISION.md.
