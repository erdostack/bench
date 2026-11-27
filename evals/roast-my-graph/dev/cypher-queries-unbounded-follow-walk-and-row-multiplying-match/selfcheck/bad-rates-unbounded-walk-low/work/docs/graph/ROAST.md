# Roast: queries/feed.cypher

Looks reasonable overall.

## Findings

### 1. follower_reach (low)

**Problem.** Could be slow for very popular listeners.

**Fix.** Monitor it.

### 2. recent_plays (medium)

**Problem.** Sorts all plays before limiting.

**Fix.** Keep a pointer to the latest plays.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
