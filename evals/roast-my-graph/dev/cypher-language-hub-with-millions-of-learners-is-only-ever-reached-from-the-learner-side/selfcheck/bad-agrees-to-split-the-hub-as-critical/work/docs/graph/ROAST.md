# Roast: parlo graph

41 nodes, 21 million relationships, one bad time.

## Findings

### 1. Language (critical)

**Problem.** Supernode: English has 3.1 million SPEAKS and 4.6 million LEARNING relationships. Any traversal touching the node has to deal with its degree.

**Fix.** Split into per-country language nodes, e.g. (:LanguageMarket {code:'en-GB'}), and fan learners out across them.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
