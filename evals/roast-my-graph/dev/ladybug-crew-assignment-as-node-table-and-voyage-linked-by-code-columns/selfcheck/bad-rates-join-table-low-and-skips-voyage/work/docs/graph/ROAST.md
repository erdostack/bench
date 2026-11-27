# Roast: fleetlog

Clean enough. Two nits.

## Findings

### 1. CrewAssignment (low)

**Problem.** Uses SERIAL for its key; a natural key might read better.

**Fix.** Optional.

### 2. Sailor.rank (medium)

**Problem.** Rank is free text.

**Fix.** Restrict to a fixed list in the tool.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
