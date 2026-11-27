# Roast: parks register

A text column walks into a design review expecting a firing squad and leaves with a raise.

## Findings

### 1. asset.kind (low)

**Problem.** Nothing stops a move from putting a zone under a part or a park under a zone: kind is checked against a list, not against depth or the parent's kind.

**Fix.** Check in move() that the target's kind is the one above the moved row's kind, or add a CHECK tying kind to depth (park 1, zone 2, asset 3, part 4).

### 2. remove (low)

**Problem.** After the row with the highest id is removed, add() hands the same id to the next row. Harmless today (no inspection can point at a removed row), but the tablets' day-old copies could show the old name for it.

**Fix.** Use INTEGER PRIMARY KEY AUTOINCREMENT semantics (sqlite_sequence) or never delete, only retire.

Verdict: no rewrite needed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
