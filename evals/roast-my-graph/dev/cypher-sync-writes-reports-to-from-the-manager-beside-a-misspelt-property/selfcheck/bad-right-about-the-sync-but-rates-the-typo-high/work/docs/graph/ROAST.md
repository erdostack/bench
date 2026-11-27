# Roast: orgline graph

Upside down, and misspelt.

## Findings

### 1. sync_reporting_lines (critical)

**Problem.** Writes REPORTS_TO from manager to employee; docs/model.md and all the queries expect employee to manager, so approver_for returns someone below the claimant and chain_of_command lists subordinates.

**Fix.** MERGE (e)-[:REPORTS_TO]->(m), then delete the existing REPORTS_TO relationships and rerun the sync.

### 2. managment_level (high)

**Problem.** Misspelt property used by the approval rule.

**Fix.** Rename everywhere now.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
