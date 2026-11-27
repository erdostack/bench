# Roast: opsmap queries

Direction smells and missing index anchors, the usual suspects.

## Findings

### 1. services_on_host (high)

**Problem.** Relationship direction smell: directed patterns are slower than undirected ones, and this query also lacks a LIMIT.

**Fix.** Drop the arrowhead only where performance requires it and add LIMIT 100 to bound the result.

### 2. host_by_serial (medium)

**Problem.** No index anchor! The query should start from an indexed property.

**Fix.** Rewrite the query to look the host up by name instead, since Host.name already has a constraint; have the agent send its hostname.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
