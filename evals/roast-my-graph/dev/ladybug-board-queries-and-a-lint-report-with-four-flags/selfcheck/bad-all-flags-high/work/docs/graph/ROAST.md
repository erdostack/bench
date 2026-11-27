# Roast: queries/boards.cypher

## Findings

### 1. reset_board (high)

**Problem.** Disconnected patterns.

**Fix.** Connect them.

### 2. export_card_titles (high)

**Problem.** No LIMIT; unbounded result.

**Fix.** Add LIMIT 100.

### 3. cards_with_any_label (high)

**Problem.** DISTINCT is wasteful.

**Fix.** Remove DISTINCT.

### 4. open_cards (high)

**Problem.** String literal could allow injection.

**Fix.** Use a parameter.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
