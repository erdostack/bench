# Roast: warmintro

## Findings

### 1. move_incoming_introductions (high)

**Problem.** Possible self-referential relationship after node merge (self-loop anti-pattern).

**Fix.** Add WHERE introducer <> c to referral_credit and top_connectors so self-loops are ignored in reports.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
