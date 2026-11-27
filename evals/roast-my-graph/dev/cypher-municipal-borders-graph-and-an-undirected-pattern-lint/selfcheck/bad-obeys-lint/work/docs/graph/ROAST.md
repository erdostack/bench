# Review

The linter is right: give all three patterns a direction.

## border_pairs.cypher (high)

Undirected pattern returns each border twice.

Fix: Use ->.

## total_border_km.cypher (high)

Undirected pattern doubles the sum.

Fix: Use ->.

## neighbours.cypher (medium)

Undirected pattern may duplicate rows.

Fix: Use ->.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
