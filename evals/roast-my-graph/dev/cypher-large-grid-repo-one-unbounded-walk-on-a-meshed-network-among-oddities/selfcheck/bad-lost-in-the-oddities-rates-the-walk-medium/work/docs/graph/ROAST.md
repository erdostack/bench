# Roast: gridmap cypher/

A lot of small things.

## Findings

### 1. upsert_work_orders (medium)

**Problem.** TODO left in the loader.

**Fix.** Resolve or ticket it.

### 2. asset_by_old_ref (medium)

**Problem.** Commented-out duplicate of the query above the live one.

**Fix.** Delete the comment.

### 3. downstream_meters (medium)

**Problem.** Variable-length pattern without an upper bound; could be slow on large inputs.

**Fix.** Consider adding a bound.

### 4. label_joints (low)

**Problem.** Four near-identical labelling statements.

**Fix.** Generate them.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
