# Review

Mostly sound. The one modelling mistake is SkillClaim: it's a relationship with two properties dressed
up as a node, and it puts an extra hop into your busiest query. Turn it into HAS_SKILL {since, level}.
Contract looks similar but is correct as a node: other things attach to it.

## SkillClaim (medium)

Problem: A claim only ever connects one freelancer to one skill and carries two values; nothing else points at it. As a node it costs an extra hop and 6.2 million extra nodes in freelancers_with_skill, the busiest query, and in the profile.

Fix: Make it a relationship: (:Freelancer)-[:HAS_SKILL {since, level}]->(:Skill). Migrate with one batched statement, then drop CLAIMS, FOR_SKILL and the SkillClaim index (index the relationship's level if the filter needs it).

## Contract (low)

Problem: Also sits between two nodes, but milestones, invoices and disputes hang off it, so it is right as a node. Mentioned only so nobody 'fixes' it the same way.

Fix: Keep it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
