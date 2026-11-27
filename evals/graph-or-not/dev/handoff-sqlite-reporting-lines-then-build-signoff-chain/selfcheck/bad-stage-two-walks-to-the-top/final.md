Added signoff_chain(conn, employee_id) to hr/approvals.py. It follows solid lines from the submitter's manager all
the way up to the top of the organisation, and stops if a manager repeats so a loop can't hang it.
