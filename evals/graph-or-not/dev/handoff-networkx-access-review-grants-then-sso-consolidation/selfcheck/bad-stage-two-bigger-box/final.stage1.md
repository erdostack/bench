Decision: in-process-library

Keep the job as it is. It already runs in networkx on review-01: 38,000 identities, 6,500 groups and 390,000
membership edges peak at about 260 MB of the box's 2 GB, and the review takes 4 minutes. The CISO's rule settles
the rest: it stays while it fits in review-01's 2 GB, and if it ever doesn't, it moves to the licensed graph
database on the certified security cluster. A bigger box is off the table (re-certification). Recorded in
docs/graph/DECISION.md, with the tripwire.
