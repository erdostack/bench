# Review

One problem: the Site MERGE runs for depot devices with no site_code. See findings.json.

## Site (medium)

Problem: MERGE on Site.code with a null code (site_code missing for depot stock) throws and rolls back the single import transaction.

Fix: FOREACH (code IN CASE WHEN row.site_code IS NULL THEN [] ELSE [row.site_code] END | MERGE (site:Site {code: code}) MERGE (d)-[:INSTALLED_AT]->(site))

Roasted with erdostack: npx skills add usergraphtheory/erdostack
