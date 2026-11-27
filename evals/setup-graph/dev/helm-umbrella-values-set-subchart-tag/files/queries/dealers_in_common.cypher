// Dealers who handled objects from both collections.
MATCH (d:Holder {kind: 'dealer'})-[:HELD]->(:Object {collection: $a}),
      (d)-[:HELD]->(:Object {collection: $b})
RETURN DISTINCT d.name AS dealer ORDER BY dealer;
