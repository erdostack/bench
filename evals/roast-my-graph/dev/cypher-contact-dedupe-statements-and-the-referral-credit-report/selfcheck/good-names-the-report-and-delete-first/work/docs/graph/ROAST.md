# Roast: warmintro

## Findings

### 1. referral_credit (critical)

**Problem.** Pays contacts for introducing themselves: after move_incoming_introductions merges a duplicate that the original introduced, the original has an INTRODUCED loop to itself.

**Fix.** Before moving anything, delete the link between the two records: MATCH (keep:Contact {id:$keep})-[r:INTRODUCED]-(dup:Contact {id:$dup}) DELETE r. Then delete existing loops.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
