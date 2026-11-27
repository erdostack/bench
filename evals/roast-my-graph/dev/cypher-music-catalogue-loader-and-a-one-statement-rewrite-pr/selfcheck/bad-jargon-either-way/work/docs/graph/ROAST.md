# Roast: vinylgraph catalogue loader

Both approaches are valid upsert patterns; benchmark and choose.

## Findings

### 1. link_artists (medium)

**Problem.** Separate MATCH-then-MERGE is the idempotent upsert pattern, but four round trips per batch add latency.

**Fix.** Benchmark the PR's single MERGE against the current version and pick the faster.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
