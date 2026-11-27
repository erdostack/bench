// GB-xxx: "gifts under 50" collection for the Christmas landing page: every live bundle under EUR 50.
// Safe to apply again after a part-way failure (docs/changes.md): MERGE on the collection and on each link.
CREATE (c:Collection {slug: 'gifts-under-50'})
SET c.title = 'Gifts under €50';

MATCH (c:Collection {slug: 'gifts-under-50'})
MATCH (b:Bundle)
WHERE b.status = 'live' AND b.priceCents < 5000
CALL (b, c) {
  CREATE (b)-[l:IN_COLLECTION]->(c)
  SET l.addedAt = datetime()
} IN TRANSACTIONS OF 10000 ROWS;
