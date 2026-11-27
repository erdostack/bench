Added sql/payer.sql as decided (recursive SQL). Invoices follow the finance links: the finance parent holds the
budget, so that is who finance invoices. It walks kind = 'finance' to the top.
