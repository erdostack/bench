# Roast: merge_customers.cypher

## Findings

### 1. SUBSCRIBED_TO (high)

**Problem.** Never moved by the merge, so drop_duplicate's detach delete cancels the duplicate's subscriptions. Same for WROTE: reviews become authorless.

**Fix.** Add move statements for SUBSCRIBED_TO (copying properties) and WROTE, or use apoc.refactor.mergeNodes([keep, dup], {properties: 'discard', mergeRels: true}).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
