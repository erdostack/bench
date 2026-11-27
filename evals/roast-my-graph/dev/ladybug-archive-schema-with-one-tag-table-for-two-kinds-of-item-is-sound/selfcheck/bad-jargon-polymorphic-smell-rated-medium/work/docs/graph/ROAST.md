# Roast: morgue schema

Smells, not bugs.

## Findings

### 1. TaggedWith (medium)

**Problem.** Polymorphic relationship table (two FROM/TO pairs): a design smell that couples two node types.

**Fix.** Consider splitting it per source table; discuss with the CTO.

### 2. Article (medium)

**Problem.** No secondary indexes on published or section.

**Fix.** Consider adding secondary indexes.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
