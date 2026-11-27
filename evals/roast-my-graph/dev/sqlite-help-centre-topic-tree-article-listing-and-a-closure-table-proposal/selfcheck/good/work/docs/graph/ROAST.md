# Roast

Review of the files as they are.

## Findings

### 1. docs/review.md (low)

**Problem.** The claim that LIKE can never use an index is wrong for this schema. SQLite turns LIKE 'prefix%' into an index range when the pattern is a literal or a single bound parameter without a leading wildcard and the column's index uses NOCASE (LIKE is case-insensitive by default). articles_under binds topic_path + '%' as one parameter, and path is declared COLLATE NOCASE, so its UNIQUE index qualifies: EXPLAIN QUERY PLAN on kb.db shows SEARCH t USING INDEX ... (path>? AND path<?). The CHECKs keep % and _ out of paths, so the pattern cannot match more than the subtree. move_topic.sql gets the same index range.

**Fix.** No closure table needed. Keep the pattern bound as a whole parameter (do not change it to :path || '%', which would lose the index) and say so in a comment.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
