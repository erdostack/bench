# Roast: deskgrid queries

Neither warning is a real problem. free_grid is meant to pair every room with every slot, that is
the grid on the screen, and it is at most 920 cells; a LIMIT 100 would break it. book_cell pairs
three single-row lookups on unique keys. I found nothing that has to change before the rollout.
Details in docs/graph/ROAST.md and findings.json.

## Findings

### 1. free_grid (low)

**Problem.** The linter is right that rooms and slots are not connected, but that is the point: the screen is every room times every slot, at most 46 x 20 = 920 cells. LIMIT 100 would cut the grid after five rooms.

**Fix.** Leave it; mark the statement as an intended product in the linter config.

### 2. book_cell (low)

**Problem.** Three lookups by unique key, one row each, so the product is a single row. The Booking.cell constraint already stops double bookings.

**Fix.** Leave it, or write each lookup as its own MATCH if you just want the linter quiet.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
