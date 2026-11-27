# Roast: labmap queries and loader

The loader builds a cartesian product; the queries look fine.

## Findings

### 1. LINK_PAIR (critical)

**Problem.** Cartesian product between a and b over 7,400 researchers.

**Fix.** Rewrite as a single connected pattern.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
