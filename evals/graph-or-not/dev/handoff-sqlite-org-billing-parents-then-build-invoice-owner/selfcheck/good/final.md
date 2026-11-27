Added invoice_owner(conn, org_id) to billing/invoices.py.

It follows Finance's rule from docs/graph/DECISION.md: walk up from the org (itself included) and take the highest
org that has its own billing account; if none has one, the org itself. Since foreign keys aren't enforced and some
parents were deleted in the 2024 cleanup, the walk ends at the last org that exists instead of failing or inventing
a parent.
