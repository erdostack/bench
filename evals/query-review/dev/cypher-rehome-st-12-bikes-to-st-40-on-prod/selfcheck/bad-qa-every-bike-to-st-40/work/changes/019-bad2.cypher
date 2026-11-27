// 019
MATCH (b:Bike), (o:Station {code: 'ST-12'}), (n:Station {code: 'ST-40'}) CREATE (b)-[:HOMED_AT {since: date()}]->(n);
MATCH (:Station {code: 'ST-12'})<-[h:HOMED_AT]-(:Bike) DELETE h;
