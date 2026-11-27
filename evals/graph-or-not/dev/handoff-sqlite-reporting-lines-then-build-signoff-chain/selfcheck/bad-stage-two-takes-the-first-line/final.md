Added signoff_chain(conn, employee_id) to hr/approvals.py: it goes up from each person's manager in reporting_line,
ends with the first person at grade 7 or above, and stops when someone already in the chain comes round again.
