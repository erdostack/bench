# Review

Mostly fine; the nightly load could be faster with CREATE.

## load_network.cypher (medium)

MERGE on every row is slow for a full nightly load.

Fix: Use CREATE for a clean rebuild.

## substation_feeders.cypher (low)

No LIMIT.

Fix: Add LIMIT 100.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
