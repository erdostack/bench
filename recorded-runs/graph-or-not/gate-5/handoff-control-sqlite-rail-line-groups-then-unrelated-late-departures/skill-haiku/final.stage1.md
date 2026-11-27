Decision: in-process-library

Do not adopt a graph database for the colour families. Grouping lines that connect through shared stations is a single whole-graph pass over 140 lines and about 2,300 line-station rows, run once a month. The line graph has at most 9,730 pairs (140 x 139 / 2, arithmetic), and a union-find grouping on a synthetic sample of that size took about 13 ms with a 135 KB peak. A plain in-process structure is enough. Recursive SQL is passed over because the job has no single starting line.

Not measured: the real line-station data (var/rail.db was not in the repo), so the true number of shared-station pairs and the number of families are unknown. The meaning of "connect" (shared station only, or other links) should be confirmed. Nothing in the repo was changed except the new file docs/graph/DECISION.md.
