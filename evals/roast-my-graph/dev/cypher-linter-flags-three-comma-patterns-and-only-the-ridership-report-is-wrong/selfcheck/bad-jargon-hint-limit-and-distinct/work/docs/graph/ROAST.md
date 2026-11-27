# Roast: metroline queries

Eager aggregation meets 48 million rows.

## Findings

### 1. line_ridership (high)

**Problem.** Cartesian expansion with eager aggregation over the Tap label: memory pressure and long GC pauses on the monthly run.

**Fix.** Add USING INDEX t:Tap(day), change to count(DISTINCT t) and put LIMIT 50 on the result; raise the transaction memory limit for the reporting user.

### 2. same_line (low)

**Problem.** Comma-separated patterns, each anchored on a unique key.

**Fix.** No change needed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
