# Roast: postroom graph

Naming conventions are the first thing a reviewer sees and the last thing this schema thought about.

## Findings

### 1. :partOf (high)

**Problem.** Relationship types must be UPPER_SNAKE_CASE. A camelCase type in a production graph is a correctness hazard: one typo in a query and it silently matches nothing.

**Fix.** Rename to PART_OF everywhere.

### 2. Issue.SentAt (high)

**Problem.** PascalCase property on a node whose other properties are snake_case. Inconsistent casing breaks tooling and will cause null reads.

**Fix.** Rename to sent_at.

### 3. load_subscribers (medium)

**Problem.** MERGE uses both email and plan, so when a plan changes a second Subscriber node is created for the same email.

**Fix.** MERGE on email only and SET s.plan = row.plan.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
