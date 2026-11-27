# Roast: parks register

## Findings

### 1. asset.path (critical)

**Problem.** Hierarchy stored as delimited text. Prefix matching on strings is fragile and returns wrong subtrees, and the GLOB forces a full table scan.

**Fix.** Replace path with parent_id and use WITH RECURSIVE for subtrees and breadcrumbs.

### 2. move (high)

**Problem.** A move rewrites every descendant row.

**Fix.** With parent_id a move is a single-row update.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
