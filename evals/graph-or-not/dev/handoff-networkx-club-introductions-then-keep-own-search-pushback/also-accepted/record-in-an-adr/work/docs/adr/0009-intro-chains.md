# 9. Intro chains

Decision: in-process-library

intro_chain vs networkx shortest_path on the 34-member, 78-tie test club: ours too long on 284 of 561 pairs, up to
5 extra introductions. networkx already a dependency, ~4 µs a lookup. Neo4j rejected.
