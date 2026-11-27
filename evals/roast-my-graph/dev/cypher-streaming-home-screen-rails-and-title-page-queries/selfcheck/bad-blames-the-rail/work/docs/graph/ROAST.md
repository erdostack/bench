# Roast: reelhouse home and title queries

The genre rail is the expensive part; precompute it.

## Findings

### 1. genre_rail (high)

**Problem.** Expands 9,000 titles from a supernode Genre and sorts them on every home screen.

**Fix.** Precompute the rails.

### 2. continue_watching (medium)

**Problem.** Expands all WATCHED.

**Fix.** Add an index on finished.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
