Decision: recursive-sql. Written up in docs/graph/DECISION.md, with a note on the proposal.

Merch fixed the strip at two steps: the product's own pairings, and what pairs with those. That is two joins on
`pairing` (taking each pair in both directions, since a pair is stored once with product_a < product_b), not an open-
ended traversal. At 180k pairings over 40k products each step reads a handful of indexed rows, comfortably inside
30 ms at 1,500 pages a second on the Postgres you have. Kofi's proposal is built around the three-step ranking merch
rejected; without it there is nothing for a graph database to do, and an in-memory copy would only add a sync.
