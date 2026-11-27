# Roast: graph/closure.cypher

## Findings

### 1. close_depot (high)

**Problem.** DETACH DELETE silently removes relationships the author may not have thought about.

**Fix.** Change to plain DELETE so the statement fails if anything is still attached.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
