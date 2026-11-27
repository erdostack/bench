# Roast: partsbin import and site queries

Partially bound MERGE; add DISTINCT to the directory and index Maker.name.

## Findings

### 1. import_parts (high)

**Problem.** MERGE semantics on a partially bound pattern can lead to duplicates.

**Fix.** Add DISTINCT to maker_directory (RETURN DISTINCT m.name) and an index on Maker.name.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
