# Roast: warmintro

## Findings

### 1. move_incoming_introductions (high)

**Problem.** The outgoing move skips `other = keep`; the incoming one does not. The README's usual duplicate is (original)-[:INTRODUCED]->(duplicate) and the original is kept, so here other is keep and MERGE writes (keep)-[:INTRODUCED]->(keep). From then on referral_credit lists the contact as one of its own introducers: the bonus is split with the customer contact itself and the real introducer gets half. top_connectors counts it as an introduction too.

**Fix.** Add WHERE other <> keep to move_incoming_introductions, mirroring the outgoing statement. Remove the loops already created: MATCH (c:Contact)-[r:INTRODUCED]->(c) DELETE r. Ask finance to re-check bonuses paid since the merges started.

### 2. top_connectors (low)

**Problem.** Scans every INTRODUCED relationship; fine for a monthly look at this size.

**Fix.** No change.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
