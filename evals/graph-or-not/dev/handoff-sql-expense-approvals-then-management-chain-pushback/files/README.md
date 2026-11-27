# spendwise

Expense reports for staff. Python 3.12 / Django, Postgres 16.

- `hr_sync` copies employees and the org chart from the HR system every night (`employee.manager_id`).
- `approvals/` decides who has to approve a report. Policy questions go to finance.
