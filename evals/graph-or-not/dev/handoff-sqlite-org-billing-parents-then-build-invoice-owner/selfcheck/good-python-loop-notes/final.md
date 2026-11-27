invoice_owner is in billing/invoices.py: it climbs parent_id from the org, remembering the highest org with a
billing account, and stops at the top or at a parent row that's gone (notes/invoice-owner.md). I ran it on a small
fixture of 8 orgs I made in memory, including a deleted parent, and it gave the expected owners.
