# Roast: approvals-graph

## Findings

### 1. remove_leaver (high)

**Problem.** DETACH DELETE is a dangerous anti-pattern that cascades silently.

**Fix.** Use plain DELETE so it fails if relationships exist, and take a backup before each run.

### 2. cost_center (low)

**Problem.** Alias spelled differently from the CostCentre label.

**Fix.** Rename to cost_centre.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
