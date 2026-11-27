# Roast: pkgatlas queries

package_page touches the License supernode; denormalise the license onto the package.

## Findings

### 1. package_page (high)

**Problem.** Two OPTIONAL MATCH clauses touch License, a supernode.

**Fix.** Store the license on the package.

### 2. refresh_license_counts (medium)

**Problem.** Counts all relationships nightly.

**Fix.** Fine but slow.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
