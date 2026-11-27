# Roast: reelbase model

The generic-relationship anti-pattern, in the wild.

## Findings

### 1. RELATED (medium)

**Problem.** Generic-relationship anti-pattern: the kind property is not indexed, so the WHERE r.kind filters cannot use an index.

**Fix.** CREATE INDEX related_kind IF NOT EXISTS FOR ()-[r:RELATED]-() ON (r.kind); and keep the single RELATED type.

### 2. Credit (low)

**Problem.** Intermediate node; justified because awards and characters attach to it.

**Fix.** Keep.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
