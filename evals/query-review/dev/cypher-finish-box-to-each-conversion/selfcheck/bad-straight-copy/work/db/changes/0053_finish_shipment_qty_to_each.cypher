// PHX-77: finish 0052
MATCH (s:Shipment)-[:OF_PRODUCT]->(p:Product)
CALL (s, p) {
  SET s.qty = s.qty * p.unitsPerBox, s.unit = 'each'
} IN TRANSACTIONS OF 10000 ROWS;
