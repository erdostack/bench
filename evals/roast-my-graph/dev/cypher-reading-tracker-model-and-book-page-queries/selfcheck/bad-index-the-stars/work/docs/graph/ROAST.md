# Roast: shelfmates model and queries

Index the stars property and the book page will be fast again.

## Findings

### 1. loved_also_loved (high)

**Problem.** Filters stars after expanding all ratings of a book.

**Fix.** Add an index on stars so the filter is fast.

### 2. shelf (low)

**Problem.** Filters on the shelf property after expanding.

**Fix.** Fine.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
