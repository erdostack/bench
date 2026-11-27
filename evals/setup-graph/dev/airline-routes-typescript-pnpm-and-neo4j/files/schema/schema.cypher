CREATE CONSTRAINT airport_code IF NOT EXISTS FOR (a:Airport) REQUIRE a.iata IS UNIQUE;
CREATE CONSTRAINT carrier_code IF NOT EXISTS FOR (c:Carrier) REQUIRE c.code IS UNIQUE;
// (:Airport)-[:ROUTE {carrier, weekly}]->(:Airport)
