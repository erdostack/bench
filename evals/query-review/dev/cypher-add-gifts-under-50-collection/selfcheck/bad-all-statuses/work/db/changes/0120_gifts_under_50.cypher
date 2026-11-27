// GB-xxx: "gifts under 50" collection for the Christmas landing page: every live bundle under EUR 50.
// Safe to apply again after a part-way failure (docs/changes.md): MERGE on the collection and on each link.
MERGE (c:Collection {slug: 'gifts-under-50'})
  ON CREATE SET c.title = 'Gifts under €50';

MATCH (c:Collection {slug: 'gifts-under-50'})
MATCH (b:Bundle)
WHERE b.priceCents < 5000
CALL (b, c) {
  MERGE (b)-[l:IN_COLLECTION]->(c)
    ON CREATE SET l.addedAt = datetime()
} IN TRANSACTIONS OF 10000 ROWS;
