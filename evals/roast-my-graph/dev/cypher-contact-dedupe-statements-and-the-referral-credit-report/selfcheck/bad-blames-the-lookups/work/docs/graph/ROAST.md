# Roast: warmintro

## Findings

### 1. move_outgoing_introductions (high)

**Problem.** MATCH (keep), (dup) is a cartesian product.

**Fix.** Combine into a single pattern.

### 2. remove_duplicate (medium)

**Problem.** Plain DELETE fails if relationships remain.

**Fix.** Use DETACH DELETE.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
