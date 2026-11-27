# Review: shelfmates queries

Scope: six queries against the schema. One finding.

## Findings

### 1. genre_top (high)

**Problem.** Schema-contradiction smell and supernode risk: the pattern fans out through Genre, which has only 48 nodes for 210,000 books, and the relationship naming is inconsistent with the rest of the file.

**Fix.** Add CREATE REL TABLE Reviewed(FROM Reader TO Book, stars INT64); to schema.cypher so the name used by the query exists, and add a LIMIT on the Genre expansion.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
