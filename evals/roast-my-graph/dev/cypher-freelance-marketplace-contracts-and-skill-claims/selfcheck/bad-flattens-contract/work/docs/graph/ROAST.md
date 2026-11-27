# Review

Both in-between nodes should become relationships.

## Contract (high)

Problem: Join-table node between Client and Freelancer; an extra hop everywhere.

Fix: Replace with (:Client)-[:CONTRACTED {rate, start, end}]->(:Freelancer).

## SkillClaim (medium)

Problem: A relationship stored as a node.

Fix: Use HAS_SKILL {since, level}.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
