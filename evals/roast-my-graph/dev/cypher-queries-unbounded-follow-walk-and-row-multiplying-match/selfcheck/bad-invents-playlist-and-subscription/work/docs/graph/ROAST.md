# Roast: queries/feed.cypher

Plenty to talk about.

## Findings

### 1. follower_reach (critical)

**Problem.** FOLLOWS* has no upper bound.

**Fix.** Bound it to two hops.

### 2. listener_stats (high)

**Problem.** The Genre match is disconnected and multiplies the rows.

**Fix.** Aggregate plays first, then count genres.

### 3. Playlist.owner_id (high)

**Problem.** Playlist stores its owner as an id property instead of a relationship.

**Fix.** Add (:Listener)-[:OWNS]->(:Playlist).

### 4. [:SUBSCRIBED_TO] (medium)

**Problem.** SUBSCRIBED_TO duplicates FOLLOWS.

**Fix.** Merge the two relationship types.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
