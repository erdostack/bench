# Roast: pkgatlas queries

related_packages hits a supernode; index License.spdx and Package.category.

## Findings

### 1. related_packages (high)

**Problem.** Supernode traversal through License causes fan-out.

**Fix.** Add an index on License.spdx and on Package.category, and lower the LIMIT to 5.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
