# Roast: opsmap queries

One query has its relationship backwards.

## Findings

### 1. owners_to_page (high)

**Problem.** RUNS_ON is traversed against its direction here.

**Fix.** Reverse it to (h)-[:RUNS_ON]->(s).

### 2. upstream_of (medium)

**Problem.** Variable-length path up to 4 hops.

**Fix.** Lower the bound to 3.

### 3. services_on_host (low)

**Problem.** ORDER BY without LIMIT.

**Fix.** Add a LIMIT.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
