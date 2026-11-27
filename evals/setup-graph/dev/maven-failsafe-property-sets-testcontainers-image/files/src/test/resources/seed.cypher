CREATE CONSTRAINT supplier_code IF NOT EXISTS FOR (s:Supplier) REQUIRE s.code IS UNIQUE;
CREATE (k:ProductLine {name: 'Kettles'}), (t:ProductLine {name: 'Toasters'}),
       (a:Supplier {code: 'S-1'}), (b:Supplier {code: 'S-2'}), (f:Factory {code: 'F-77'}),
       (k)-[:BUYS_FROM]->(a), (t)-[:BUYS_FROM]->(b),
       (a)-[:SOURCES_FROM]->(f), (b)-[:SOURCES_FROM]->(f);
