// INV-512: write off the pallets the November cycle count marked lost (wh-east)
// Reviewed by: (pending)
CALL apoc.periodic.iterate(
  "MATCH (p:Pallet) WHERE p.status = 'lost' RETURN p",
  "OPTIONAL MATCH (p)-[s:STORED_IN]->() DELETE s SET p:WrittenOff, p.writtenOffAt = datetime() REMOVE p:Pallet",
  {batchSize: 2000, parallel: false}
);
