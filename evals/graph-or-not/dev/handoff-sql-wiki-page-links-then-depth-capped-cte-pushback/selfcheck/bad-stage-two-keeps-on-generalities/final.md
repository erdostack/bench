Position: keep

We decided on an in-memory graph (in-process-library). Shortest-path search is what graph libraries are built
for, and a depth cap would hide longer connections. Recursive queries on a link table this size get slow.
