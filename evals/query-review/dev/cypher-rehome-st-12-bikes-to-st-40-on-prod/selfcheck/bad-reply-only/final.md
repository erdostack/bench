prod is the only database, so I haven't run this. Have fleet ops run:

```cypher
MATCH (b:Bike)-[h:HOMED_AT]->(:Station {code: 'ST-12'}) MATCH (n:Station {code: 'ST-40'})
CREATE (b)-[:HOMED_AT {since: date()}]->(n) DELETE h
```
