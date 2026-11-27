# Roast: deskgrid queries

The linter is right: two cartesian products. Add the LIMIT and split book_cell.

## Findings

### 1. free_grid (high)

**Problem.** Cartesian product of Room and Slot; grows with every room added.

**Fix.** Add LIMIT 100 and paginate.

### 2. book_cell (high)

**Problem.** Three-way cartesian product.

**Fix.** Split into separate MATCH steps.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
