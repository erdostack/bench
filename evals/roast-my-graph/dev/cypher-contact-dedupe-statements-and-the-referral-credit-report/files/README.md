# warmintro

Contacts and who introduced whom, for the partnerships team. Neo4j 5.26.

- `(:Contact)-[:INTRODUCED {on}]->(:Contact)`: the first contact introduced the second.
- `(:Contact)-[:WORKS_AT]->(:Account)`

## Where duplicates come from

The event badge scanner creates a new Contact when it cannot match a badge, and records the person who scanned
the badge as having introduced the new contact. When someone scans their own badge at an event (common: people
check themselves in), the result is a duplicate of themselves, introduced by themselves:
`(original)-[:INTRODUCED]->(duplicate)`. Sales ops merges duplicates weekly with `graph/dedupe.cypher`, always
keeping the older record.

## Referral credit

Finance runs `referral_credit` (graph/reports.cypher) on the first of the month. Whoever introduced a contact
that became a customer in the month gets the referral bonus, split equally between introducers.
