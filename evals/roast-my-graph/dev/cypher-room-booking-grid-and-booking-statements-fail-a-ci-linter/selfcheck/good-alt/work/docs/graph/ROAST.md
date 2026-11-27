# Roast: deskgrid queries

The two linter warnings are false alarms. free_grid's product is the grid itself (46 rooms x 20
slots in the biggest building) and book_cell's lookups are one row each by unique key. Don't add
the LIMIT. Only a cosmetic note about the string day.

## Findings

### 1. Booking.day (low)

**Problem.** day is stored and compared as a string; consistent everywhere, so it works.

**Fix.** Optional: store it as a date.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
