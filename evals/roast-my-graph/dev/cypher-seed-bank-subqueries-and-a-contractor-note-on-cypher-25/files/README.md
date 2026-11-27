# seedvault

Inventory of a regional seed bank. `(:Accession {code})-[:STORED_IN]->(:Drawer {code})`,
`(:Accession)-[:OF_TAXON]->(:Taxon {name})`, `(:Accession)-[:TESTED]->(:GerminationTest {tested_on, sown, sprouted})`.
~48,000 accessions, 210,000 germination tests.
