Decision: in-process-library. Written up in docs/adr/0007-crash-grouping.md.

Grouping is connected components over the week's reports: 4M nodes and 11M links. The SQL job does it by label
propagation, one full UPDATE per pass, and took 5 h 40 min against a 1 hour window. networkx did the same week in
9 minutes with a 19 GB peak on a 64 GB box that is idle at night. So: read the week's links in the nightly job,
connected_components in memory, write issue ids back in one batch. No new server, Python as you have it.
