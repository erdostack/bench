// Everyone who held $id, in order.
MATCH (h:Holder)-[r:HELD]->(:Item {id: $id})
RETURN h.name, h.kind, r.since, r.until
ORDER BY r.since;
