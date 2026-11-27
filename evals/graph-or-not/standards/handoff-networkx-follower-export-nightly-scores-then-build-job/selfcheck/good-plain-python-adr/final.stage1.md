Decision: in-process-library

Load the export into memory on the batch box and compute both scores there; 2.8M follows is small for 8 GB and the
window is 02:30 to 06:00. No Neo4j. Recorded in docs/adr/0003-nightly-scores.md, including the rule that muted
follows give no reach but still join rings.
