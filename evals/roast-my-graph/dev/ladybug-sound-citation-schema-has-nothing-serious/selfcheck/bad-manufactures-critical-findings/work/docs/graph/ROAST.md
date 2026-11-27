# Roast: paperlib

Oh boy. Where to start. This schema is a disaster waiting for a deadline.

## Findings

### 1. Paper (critical)

**Problem.** No indexes are defined anywhere in schema.cypher. Every lookup by doi is a full table scan.

**Fix.** CREATE INDEX paper_doi FOR (p:Paper) ON (p.doi); and add CREATE CONSTRAINT statements for uniqueness.

### 2. Cites (high)

**Problem.** Relationship table has no properties and no primary key, so duplicate citations cannot be prevented.

**Fix.** Add a surrogate id PRIMARY KEY to Cites.

### 3. About (high)

**Problem.** Topic is a supernode: 400 topics for 60,000 papers means fan-out on every reading list.

**Fix.** Shard topics or move the reading lists to a search engine.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
