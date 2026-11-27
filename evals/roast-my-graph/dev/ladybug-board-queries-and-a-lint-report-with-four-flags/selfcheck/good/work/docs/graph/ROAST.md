# Roast: queries/boards.cypher

## Findings

### 1. reset_board (critical)

**Problem.** The second MATCH (l:Label) WHERE l.name STARTS WITH 'tmp-' has nothing tying the label to board b. Reset therefore deletes every temporary label in the database (every tenant that is in triage loses its labels and the TAGGED links on its cards), not just this board's. The README says Reset must not touch other boards or tenants. Each card is also paired with every such label, but that is the smaller problem.

**Fix.** Delete the board's own temporary labels through LABEL_FOR, and the cards separately:
MATCH (l:Label)-[:LABEL_FOR]->(b:Board {id: $board_id}) WHERE l.name STARTS WITH 'tmp-' DETACH DELETE l;
MATCH (c:Card)-[:ON_BOARD]->(b:Board {id: $board_id}) DETACH DELETE c;

### 2. export_card_titles (low)

**Problem.** NO_LIMIT is a false alarm: a board has at most 500 cards and the export must include them all.

**Fix.** Suppress the rule here.

### 3. cards_with_any_label (low)

**Problem.** DISTINCT_WASTEFUL is wrong: a card tagged with two of the labels matches twice, so DISTINCT is what makes the count right.

**Fix.** Keep DISTINCT; suppress the rule.

### 4. open_cards (low)

**Problem.** STRING_LITERAL is a false alarm: 'archived' is a constant, not user input.

**Fix.** No change, or make it a parameter purely to quiet the linter.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
