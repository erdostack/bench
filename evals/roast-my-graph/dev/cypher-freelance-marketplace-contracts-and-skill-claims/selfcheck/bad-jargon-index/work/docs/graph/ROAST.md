# Review

Reified skill claims are fine but need a composite index for the search.

## SkillClaim (medium)

Problem: Intermediate-node pattern (reification) without a composite index causes slow skill search.

Fix: Add a composite index on SkillClaim(level, since).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
