// name: accession_card
MATCH (b:Accession {code: $code})-[:OF_TAXON]->(t:Taxon)
OPTIONAL MATCH (b)-[:STORED_IN]->(d:Drawer)
CALL (b) {
  OPTIONAL MATCH (b)-[:TESTED]->(g:GerminationTest)
  RETURN max(g.tested_on) AS last_test,
         CASE WHEN sum(g.sown) > 0 THEN sum(g.sprouted) * 1.0 / sum(g.sown) END AS germination_rate
}
RETURN b.code, t.name, d.code AS drawer, last_test, germination_rate;

// name: taxon_holdings
MATCH (t:Taxon {name: $taxon})
CALL (t) {
  MATCH (t)<-[:OF_TAXON]-(b:Accession)
  RETURN count(b) AS accessions, sum(b.grams) AS grams
}
RETURN t.name, accessions, grams;

// name: viability_alerts
MATCH (g:GerminationTest)<-[:TESTED]-(b:Accession)
WHERE g.tested_on >= date() - duration('P1Y')
  AND g.sprouted * 1.0 / g.sown < 0.6
RETURN b.code, g.tested_on, g.sprouted, g.sown
ORDER BY g.tested_on DESC;

// name: drawer_contents
MATCH (d:Drawer {code: $drawer})<-[:STORED_IN]-(b:Accession)-[:OF_TAXON]->(t:Taxon)
RETURN b.code, t.name, b.grams
ORDER BY t.name, b.code;
