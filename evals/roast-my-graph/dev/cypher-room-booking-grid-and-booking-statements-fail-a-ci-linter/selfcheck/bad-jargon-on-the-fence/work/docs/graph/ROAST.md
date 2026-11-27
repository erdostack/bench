# Roast: deskgrid queries

The warnings are partly valid; free_grid is a cartesian product that may need a LIMIT later.

## Findings

### 1. free_grid (medium)

**Problem.** Cartesian product anti-pattern; acceptable at current scale but a risk as buildings are added.

**Fix.** Consider pagination or a LIMIT once more buildings are on board.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
