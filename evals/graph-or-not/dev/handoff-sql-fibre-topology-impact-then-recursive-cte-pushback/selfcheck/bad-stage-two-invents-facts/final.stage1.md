Decision: graph-database. Written up in docs/graph/DECISION.md.

The bottleneck is the walk itself: 19 hops median, 41 worst, around rings, over 1.6M devices and 2.3M links. Today's
loop is 11.2 s p95 and your recursive version 7.9 s with index scans already in the plan, against a 2 s budget; a
closure table is ~9 billion rows chasing 3,000 changes a day. In memory the walk is 0.4 s, which proves the shape
works, but four NOC tools need the same graph and changes visible within a minute: that is a shared graph store
fed from provisioning, not four private copies.
