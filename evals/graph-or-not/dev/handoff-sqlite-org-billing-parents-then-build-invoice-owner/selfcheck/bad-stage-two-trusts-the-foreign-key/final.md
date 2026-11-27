Added invoice_owner(conn, org_id) to billing/invoices.py: it climbs parent_id to the top and returns the highest
org with its own billing account, or org_id when there is none.
