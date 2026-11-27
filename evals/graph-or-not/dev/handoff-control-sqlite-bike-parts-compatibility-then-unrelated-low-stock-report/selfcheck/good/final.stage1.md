Decision: no-graph

"Fits with" is a single lookup: the rows of compat where the part is on either side. Nothing is followed further,
because the supplier says compatibility doesn't carry over. Noted in docs/graph/DECISION.md.

- 40k pairs with the primary key on (part_a, part_b) and an index on part_b: microseconds, at 30 views a minute.
- A graph database would be a second copy of the catalogue to rebuild every week, for a one-step lookup.
