I added `signoff_chain(conn, employee_id)` to `hr/approvals.py`. It returns the ids of the approvers for a claim from that employee, in order, starting with their line manager. The submitter is not in the list.

It follows only `solid` reporting lines, because `dotted` leads are functional or project leads rather than line approvers. The schema allows one solid line per employee, so the walk is unambiguous. It stops when an employee has no solid manager, and it also stops if the export contains a cycle, so it cannot loop forever.

I checked it against an in-memory copy of `db/schema.sql` with a small sample: a three-level chain returns the managers in order, a top-of-line employee returns an empty list, and a cycle terminates. I did not change anything else, including the TODO comment and the approval page.
