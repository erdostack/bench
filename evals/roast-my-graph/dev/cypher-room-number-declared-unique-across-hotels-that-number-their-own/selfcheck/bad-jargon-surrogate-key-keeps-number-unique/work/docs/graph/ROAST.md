# Roast: innkeep graph

Natural keys: convenient until the painters arrive.

## Findings

### 1. Room.number (high)

**Problem.** Natural key anti-pattern: the business identifier is used as the node key under a uniqueness constraint. Natural keys are mutable (refurbishments renumber rooms) and cause cascading updates.

**Fix.** Introduce a surrogate key Room.id (UUID) and keep the uniqueness constraint on number as a secondary business rule.

### 2. load_rooms (medium)

**Problem.** MERGE followed by SET rewrites every property on each load.

**Fix.** Use ON CREATE SET / ON MATCH SET.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
