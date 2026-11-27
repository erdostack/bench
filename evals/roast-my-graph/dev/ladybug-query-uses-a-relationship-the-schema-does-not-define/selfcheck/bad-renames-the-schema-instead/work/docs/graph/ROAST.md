# Review: shelfmates queries

Scope: six queries against the schema. Two findings.

## Findings

### 1. Rated (high)

**Problem.** Relationship table is misnamed; the queries expect Reviewed.

**Fix.** Rename Rated to Reviewed in schema.cypher and update shelf, book_rating and friends_liked.

### 2. genre_top (medium)

**Problem.** Sorting by average with no minimum vote count lets a single rating dominate.

**Fix.** Add HAVING-style filter: WHERE votes >= 5 after a WITH.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
