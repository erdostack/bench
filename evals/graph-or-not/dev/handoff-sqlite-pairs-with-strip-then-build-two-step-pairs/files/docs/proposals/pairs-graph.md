# Proposal: a graph behind "pairs with"

Author: Kofi. Status: draft.

Merchandising curate pairings by hand. Treated as a graph, they give us much more than the direct pairings: if a
lamp pairs with a side table and the side table pairs with a rug, the lamp probably goes with the rug as well.

Proposal:

- Copy `pairing` into a graph database and keep it in sync from the admin.
- For the strip, take everything up to three steps away from the product and rank it by the number of distinct
  paths that reach it.
- Later: personalised suggestions from purchase history on the same graph.

I made a mock-up of the strip with three steps for the merch team to try.
