Decision: need-more-information. Written up in docs/graph/DECISION.md.

How many steps does the badge look: 2, or up to 6? That decides it. At 2 steps it is a fixed lookup over indexed
follows (a few hundred rows per view): stay on SQLite. At 6 steps over 6.4M follows the walk reaches a large part of
380k members on every view, at 70 views a second inside 150 ms, and the question becomes precomputing, not which
database. Neo4j does not answer that either. Tell me the depth after the meeting.
