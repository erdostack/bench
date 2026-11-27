# Roast: pawprint model

Intermediate nodes: sometimes a hyperedge, sometimes a habit.

## Findings

### 1. Visit (medium)

**Problem.** Visit is a reified relationship (a hyperedge between Animal, Vet and Drug). Reification is a legitimate pattern, but it costs an extra hop on animal_record and day_sheet, and the textbook guidance is to prefer a qualified relationship when the intermediate node has low fan-out.

**Fix.** Consider collapsing Visit into a qualified (:Animal)-[:SEEN_BY]->(:Vet) relationship and benchmark both shapes before the rollout; there are arguments either way.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
