# Review: sopgraph

You don't have to rewrite either query; the linter can't see what makes them safe. Both start from a single step and follow NEXT, and NEXT only ever exists between one step and the next within one procedure version, written by the loader, which refuses more than 40 steps. So each walk is one straight chain of at most 40 steps. If the build must pass, writing *0..40 and *..40 costs nothing and records the limit. I found nothing serious elsewhere.

## Findings

### 1. queries/steps_remaining.cypher (low)

**Problem.** Flagged by the linter as unbounded, but the chain it follows has at most 40 steps (MAX_STEPS in loader/load.py), so it returns at most 39 rows. The only weakness is that the limit lives in the loader, not in the query.

**Fix.** Write [:NEXT*..40] so the build passes and the query documents the limit.

### 2. queries/steps_in_order.cypher (low)

**Problem.** Same as above: a walk along one chain of at most 40 steps.

**Fix.** [:NEXT*0..40], or keep it and suppress W012 with a comment pointing at MAX_STEPS.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
