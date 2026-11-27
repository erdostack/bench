Decision: in-process-library. Written up in docs/graph/DECISION.md.

21,900 derivation rows from a nightly export, chains up to 6 steps, a few recalls a month, and networkx is already
here: load the export and take the descendants. Two rules go with it: ids are compared without case or trailing
spaces (the 212 LIMS B ids), and destroyed tubes are left off the list while the walk continues through them.
Neo4j would be a server for a few queries a month.
