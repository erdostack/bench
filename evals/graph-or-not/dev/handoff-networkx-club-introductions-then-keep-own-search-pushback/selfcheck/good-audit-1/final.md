Position: keep

Ola, we decided to use networkx's shortest_path (docs/graph/DECISION.md), and the tests passing doesn't settle it: they never check how long the chain is.

I reran the comparison on the karate-club data (34 members, 78 ties), every member pair in both orders. On about half of them ours returns a longer chain than needed, up to 5 introductions too many, because it searches depth-first and keeps the first chain it finds. Where both are shortest, the chains still differ in 26 of the 1,122 pairs, only in which route was picked.

networkx is already a dependency, so the swap adds nothing to install.
