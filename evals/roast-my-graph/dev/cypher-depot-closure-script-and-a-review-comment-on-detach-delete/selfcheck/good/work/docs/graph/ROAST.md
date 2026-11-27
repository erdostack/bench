# Roast: graph/closure.cypher

## Findings

### 1. tools/close_depot.py (low)

**Problem.** Statements are found by splitting closure.cypher on ';' and picked by position (STATEMENTS[:2], STATEMENTS[2]); reordering the file or adding a ';' inside a comment would run the wrong statement.

**Fix.** Pick statements by their // name: comment, or keep them as named constants in the tool.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
