# Roast: parlo graph

Supernode risk, deferred.

## Findings

### 1. Language (medium)

**Problem.** High-degree node: 7.7 million relationships on English. Supernode risk for any query touching it.

**Fix.** Monitor and partition by country if latency degrades; consider doing it pre-launch to be safe.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
