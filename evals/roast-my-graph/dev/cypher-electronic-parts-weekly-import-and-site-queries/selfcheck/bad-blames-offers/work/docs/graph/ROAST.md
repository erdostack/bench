# Roast: partsbin import and site queries

import_offers can drop offers; MERGE the part. The rest is fine.

## Findings

### 1. import_offers (high)

**Problem.** MATCH then MERGE: if the part is missing, the offer is silently dropped.

**Fix.** MERGE the part instead of MATCH.

### 2. maker_directory (medium)

**Problem.** Scans every Maker.

**Fix.** Precompute counts.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
