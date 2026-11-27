# Roast: pkgatlas queries

The p99 jump is related_packages: it walks from the package to its license and out to every other
package under the same license, 1.5 million for MIT, on every page view. Precompute the related
list nightly instead. package_page and license_page are fine. Details in docs/graph/ROAST.md and
findings.json.

## Findings

### 1. related_packages (critical)

**Problem.** To find similar packages it goes from the package to its license and back out to every package with that license: 1.52 million for MIT, 610,000 for ISC. Each package page view reads all of them, checks their category and sorts by downloads, to keep 8. That is the p99 jump, and it runs 900 times a second.

**Fix.** Do not walk the license per request. Compute the 8 related packages per package in the nightly job and store them as (:Package)-[:RELATED {rank}]->(:Package); the page then reads 8 relationships.

### 2. package_page (low)

**Problem.** Reaches the license from the package side, one hop to one node; cheap.

**Fix.** Nothing.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
