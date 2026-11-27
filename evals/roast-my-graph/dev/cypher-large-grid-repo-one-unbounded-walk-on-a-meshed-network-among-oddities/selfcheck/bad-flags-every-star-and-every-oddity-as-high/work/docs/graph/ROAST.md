# Roast: gridmap cypher/

Unbounded variable-length paths, unindexed lookups, integer timestamps. The full set.

## Findings

### 1. zone_rollup (critical)

**Problem.** Unbounded variable-length pattern (WITHIN*0..). Unbounded traversals are never acceptable in production Cypher.

**Fix.** Add an upper bound.

### 2. downstream_meters (critical)

**Problem.** Unbounded variable-length pattern over CONNECTS on a meshed network: path explosion.

**Fix.** Bound the hops and exclude normally_open cables.

### 3. asset_by_old_ref (high)

**Problem.** Unindexed lookup on legacy_ref scans 410,000 nodes.

**Fix.** Create an index on Asset.legacy_ref.

### 4. installed_ms (high)

**Problem.** Epoch integers instead of temporal types break date arithmetic.

**Fix.** Migrate to datetime.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
