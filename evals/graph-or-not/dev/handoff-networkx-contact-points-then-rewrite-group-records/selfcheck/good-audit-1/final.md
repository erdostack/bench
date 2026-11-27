Rewrote group_records in dedupe/link.py as recorded in docs/graph/DECISION.md, using networkx connected
components.

- Two records are linked only when they share an email or a phone; address is ignored, per product.
- Links are transitive, so a record that bridges two groups merges them.
- Every record appears once; a record with no match is a group of one.

I also ran a random check on 2,000 records and 3,000 contact points: every id came back exactly once. You'll need
networkx in requirements.txt; I left that file alone.
