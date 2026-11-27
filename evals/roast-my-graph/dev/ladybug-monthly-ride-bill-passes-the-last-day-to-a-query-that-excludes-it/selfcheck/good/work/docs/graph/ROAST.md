# Roast: pedalpool billing

Started from the complaint: the attached list and the total disagree.

## Findings

### 1. account_totals (critical)

**Problem.** billing/periods.py makes last_day the last day of the month, inclusive, and bill_month passes it to both queries. account_statement filters ended_on <= $last_day, but account_totals filters ended_on < $last_day, so every ride that ended on the last day is missing from the rides, minutes and amount on the invoice. The next month's period starts on its 1st, so those rides are never billed in any month. The statement lists them, hence invoices whose total does not match their list. Lost revenue is at least one day per month, and the README says the last working day is a busy one.

**Fix.** Use one convention. Either change account_totals to r.ended_on <= $last_day, or make the period end exclusive (first day of the next month) and use < in both queries. Then bill the last days of the past months that were missed.

### 2. billable_accounts (low)

**Problem.** Runs account_totals and account_statement once per account, 1,400 accounts, so 2,800 queries in the monthly run. Fine for a monthly job in an embedded database.

**Fix.** Nothing needed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
