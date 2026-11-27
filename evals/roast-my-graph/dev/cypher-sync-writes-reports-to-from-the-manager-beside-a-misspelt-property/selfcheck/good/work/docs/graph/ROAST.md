# Roast: orgline graph

An org chart that is perfectly accurate if you hold it upside down. The expenses tool has been holding it the right way up.

## Findings

### 1. sync_reporting_lines (critical)

**Problem.** The statement matches the employee as e and the manager as m and then writes MERGE (m)-[:REPORTS_TO]->(e), so the stored relationship runs from manager to employee. docs/model.md defines it from the employee to the manager, and chain_of_command, approver_for, direct_reports and headcount_under all read it that way. Against the data as written they return the opposite: approver_for follows the arrows away from the claimant and reaches people below them, so an expense claim is routed to one of the claimant's own reports, and an employee with no reports gets no approver at all. chain_of_command shows subordinates, direct_reports shows the one manager, headcount_under counts the bosses.

**Fix.** Write it the way the model says: MERGE (e)-[:REPORTS_TO]->(m). The stored relationships repair themselves on the next run, because clear_lines removes them all and the corrected statement writes them again; run the sync once by hand if you do not want to wait for tonight. Leave the queries and the doc as they are.

### 2. clear_lines (low)

**Problem.** Removes about 145,000 relationships and the sync writes them back, every night, in one transaction. It works at this size and it is why a wrong line never lingers, but for those seconds the transaction is large.

**Fix.** Fine for now. If the company grows a lot, compare the export with the graph and change only what differs.

### 3. managment_level (low)

**Problem.** Misspelt, in the sync, the queries, the index and the doc alike. It works because the spelling is the same everywhere.

**Fix.** Rename when convenient, in one change across all four places.

### 4. tmp_idx_2 (low)

**Problem.** An index name that says nothing about what it covers.

**Fix.** Recreate it as employee_management_level when the property is renamed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
