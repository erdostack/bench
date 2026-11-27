Position: keep

Ola, the tests pass because they don't check length. We compared intro_chain with networkx's shortest_path on all
561 pairs in the karate-club test data (34 members, 78 ties) and ours returned a longer chain than needed on 284 of
them, up to 5 introductions too many. That's the complaints. It searches depth-first and stops at the first chain.
networkx is already a dependency for the stats page and takes about 4 µs per lookup, so the decision stands: use
its shortest_path (docs/graph/DECISION.md). Happy to add a test that checks chain length.
