Done: signoff_chain(conn, employee_id) in hr/approvals.py, one recursive query following ADR 0003. Solid lines
only, it ends with the first person at grade 7 or above, and it carries the path so the loops in the export end
the chain instead of going round. I checked it on a toy directory I made in memory: a ring of 3 gives 2 approvers.
