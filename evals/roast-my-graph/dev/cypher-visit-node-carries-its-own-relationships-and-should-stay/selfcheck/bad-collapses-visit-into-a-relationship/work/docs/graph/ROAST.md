# Roast: pawprint model

Your tech lead is right, and the join table is not even wearing a good costume.

## Findings

### 1. Visit (critical)

**Problem.** Classic reified relationship: an intermediate node whose only job is to connect an Animal to a Vet. It doubles the hop count of every traversal and adds 1.3 million nodes that are really edges.

**Fix.** Replace it with (:Animal)-[:SEEN_BY {day, slot, reason, notes, weight_kg}]->(:Vet) and store prescriptions as a list property on that relationship.

### 2. FOLLOW_UP_OF (high)

**Problem.** Visit-to-visit chains are a symptom of the reification; they disappear once Visit is a relationship.

**Fix.** Keep a follow_up_of_day property on the SEEN_BY relationship instead.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
