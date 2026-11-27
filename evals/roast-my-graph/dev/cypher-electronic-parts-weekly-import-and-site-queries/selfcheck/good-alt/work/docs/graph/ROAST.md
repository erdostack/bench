# Roast: partsbin import and site queries

import_parts creates a Maker per part; merge Maker separately and constrain Maker.name.

## Findings

### 1. MADE_BY merge in import/weekly.cypher (high)

**Problem.** Duplicate Maker nodes: the Maker is part of the unbound MERGE, so it is created anew for each part.

**Fix.** WITH p, row MERGE (m:Maker {name: row.maker}) MERGE (p)-[:MADE_BY]->(m); clean up the copies.

### 2. Maker.name (medium)

**Problem.** Indexed but not unique.

**Fix.** Make it a uniqueness constraint.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
