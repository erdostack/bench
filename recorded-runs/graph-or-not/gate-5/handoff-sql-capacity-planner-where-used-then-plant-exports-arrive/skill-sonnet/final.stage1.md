Decision: need-more-information

I can't responsibly pick between the options yet, because the size of the Brno and Pune BOMs is unknown, and it decides the answer. Nothing in the repo was changed except the new file docs/graph/DECISION.md.

What I can say:
- This is a real graph traversal (an upward walk of any depth over bom_line), so "not a graph problem" is out.
- Today fails the budget: 40,000 x 90 ms = 3,600 s, an hour, against 600 s. Staying with one statement per component would need 15 ms each, 6 times faster than now. The bom_line_component index is already there, so it is not a missing index.
- Linz alone is small. I measured a networkx graph at about 456 bytes per edge (synthetic sample, networkx 3.7), so Linz's 180,000 lines is about 82 MB. Your 2 GB holds about 4.7 million edges at that cost, about 26 times Linz, less if the planner needs copies in more than one process.
- So: if Brno plus Pune stay under roughly that, networkx in the planner, loaded nightly, is the likely answer. If Pune is far above it, the answer moves to a graph database (or a compact service), unless a recursive SQL rewrite is shown to meet 10 minutes. A graph database is not justified by the evidence so far; Linz is tiny and nobody has tried a rewrite.

What I need, in order of value:
1. BOM line counts for Brno and Pune, even as a rough range, and whether they are separate graphs per plant.
2. For Linz, `EXPLAIN (ANALYZE, BUFFERS)` of sql/where_used.sql on Postgres for a typical and the largest changed component (rows in the Recursive Union versus distinct assemblies returned).
3. The number of distinct assemblies above all 40,000 changed components in one run; if it is much smaller than 40,000 times the per-component set, one batched walk could meet the 10 minutes at any size.
4. How many planner processes or hosts would each hold a copy.
5. Any timing record of Linz runs, to check 90 ms is typical and not skewed by a few deep components.

I did not run anything against real data: there is no database or export in the repo. Details are in docs/graph/DECISION.md.
