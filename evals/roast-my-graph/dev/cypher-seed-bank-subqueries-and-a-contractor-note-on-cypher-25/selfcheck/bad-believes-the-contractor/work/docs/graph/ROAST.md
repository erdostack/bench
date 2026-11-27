# Review

He's right, rewrite both subqueries with importing WITH.

## accession_card (high)

Problem: Cypher 25 syntax on a 5.x server.

Fix: Rewrite as CALL { WITH b ... }.

## taxon_holdings (high)

Problem: Cypher 25 syntax on a 5.x server.

Fix: Rewrite as CALL { WITH t ... }.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
