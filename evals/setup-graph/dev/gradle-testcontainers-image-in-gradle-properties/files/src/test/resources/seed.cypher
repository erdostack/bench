CREATE (b:Venue {name: 'The Barn'}), (h:Venue {name: 'Harbour Hall'}),
       (i:Person {name: 'Ines'}), (t:Person {name: 'Tom'}), (r:Person {name: 'Ravi'}),
       (i)-[:CERTIFIED_FOR]->(b), (t)-[:CERTIFIED_FOR]->(b), (r)-[:CERTIFIED_FOR]->(h);
