// Run in order with $keep and $dup, in one transaction (tools/merge_contacts.py).

// name: move_outgoing_introductions
MATCH (keep:Contact {id: $keep}), (dup:Contact {id: $dup})
MATCH (dup)-[r:INTRODUCED]->(other:Contact)
WHERE other <> keep
MERGE (keep)-[n:INTRODUCED]->(other)
  ON CREATE SET n.on = r.on
DELETE r;

// name: move_incoming_introductions
MATCH (keep:Contact {id: $keep}), (dup:Contact {id: $dup})
MATCH (other:Contact)-[r:INTRODUCED]->(dup)
MERGE (other)-[n:INTRODUCED]->(keep)
  ON CREATE SET n.on = r.on
DELETE r;

// name: move_employment
MATCH (keep:Contact {id: $keep}), (dup:Contact {id: $dup})
MATCH (dup)-[w:WORKS_AT]->(a:Account)
MERGE (keep)-[:WORKS_AT]->(a)
DELETE w;

// name: remove_duplicate
MATCH (dup:Contact {id: $dup})
WHERE NOT (dup)--()
DELETE dup;
