# Review

Classic supernode problem in related_guides; index Topic.slug and reduce the LIMIT.

## related_guides (high)

Problem: Supernode traversal: unindexed Topic lookup causes full scan.

Fix: Create an index on Topic.slug and lower LIMIT to 3.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
