# Review

He's right; Loan is a leftover join table. Flatten it.

## Loan (high)

Problem: Join-table node; costs a hop on every loan query.

Fix: Replace with (:Member)-[:BORROWED {out, due, returned}]->(:Copy); move fines onto the member.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
