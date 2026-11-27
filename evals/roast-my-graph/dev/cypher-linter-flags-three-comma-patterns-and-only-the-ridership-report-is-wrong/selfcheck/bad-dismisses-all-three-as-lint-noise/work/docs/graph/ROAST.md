# Roast: metroline queries

Linters gonna lint.

## Findings

### 1. line_ridership (medium)

**Problem.** Cross-product cardinality warning; the predicate on t.day keeps it manageable but the planner may not pick the tap_day index for the range.

**Fix.** Add USING INDEX t:Tap(day) and a LIMIT 50 so the report stays bounded.

### 2. zone_pairs (low)

**Problem.** Self-join on Zone.

**Fix.** Fine at six zones.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
