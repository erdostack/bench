# Roast: merge_customers.cypher

## Findings

### 1. drop_duplicate (critical)

**Problem.** Only PLACED, LIVES_AT and REFERRED are moved. model.md also has WROTE and SUBSCRIBED_TO, and DETACH DELETE removes them without complaint: the duplicate's reviews lose their author (product_reviews stops showing them) and its paid subscriptions disappear, so billing stops delivering. Three hundred merges a week.

**Fix.** Before drop_duplicate, move both: MATCH (keep:Customer {id:$keep}), (dup:Customer {id:$dup}) MATCH (dup)-[w:WROTE]->(r:Review) CREATE (keep)-[:WROTE]->(r) DELETE w; and for SUBSCRIBED_TO create the new relationship with SET n = s to copy since and next_delivery, then DELETE s. Then make drop_duplicate MATCH (dup:Customer {id:$dup}) WHERE NOT (dup)--() DELETE dup and fail the merge if nothing was deleted, so a new relationship type can't be lost silently.

### 2. move_referrals (low)

**Problem.** Guards both directions against keep, so no self-referral; the two OPTIONAL MATCHes pair every outgoing with every incoming referral, which only repeats idempotent MERGEs.

**Fix.** Optional: split into two statements.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
