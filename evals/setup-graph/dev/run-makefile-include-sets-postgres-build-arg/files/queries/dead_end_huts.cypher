MATCH (h:Hut) WHERE NOT (h)-[:PATH]->()
RETURN h.name
