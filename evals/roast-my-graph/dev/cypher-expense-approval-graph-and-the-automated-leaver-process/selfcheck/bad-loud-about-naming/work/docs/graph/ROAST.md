# Roast: approvals-graph

## Findings

### 1. cost_center (high)

**Problem.** Inconsistent spelling between cost_center and CostCentre will confuse every consumer of the report.

**Fix.** Pick one spelling across the codebase.

### 2. spend_by_cost_centre (medium)

**Problem.** Unbounded REPORTS_TO*0.. walk.

**Fix.** Bound it to *0..8.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
