# Roast: queries/boards.cypher

## Findings

### 1. reset_board (high)

**Problem.** Deletes other tenants' data: the label part of the query isn't joined to the board, so all tmp- labels everywhere go.

**Fix.** Join labels to the board: MATCH (b)<-[:LABEL_FOR]-(l:Label) WHERE l.name STARTS WITH 'tmp-'.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
