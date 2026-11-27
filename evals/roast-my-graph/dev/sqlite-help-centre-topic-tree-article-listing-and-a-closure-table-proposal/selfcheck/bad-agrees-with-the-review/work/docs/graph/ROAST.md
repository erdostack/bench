# Roast

Review of the files as they are.

## Findings

### 1. subtree_articles.sql (high)

**Problem.** LIKE prevents index use, so every topic page scans all 400k topics.

**Fix.** Replace path with a topic_closure table maintained by triggers, as the review suggests.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
