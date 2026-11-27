# Invoicing rules

These come from our accountant and the tax rules we invoice under.

- An invoice, once issued, never changes. It must show the customer's name, billing address and VAT number
  as they were on the day it was issued, and each item as we described and priced it on that day. If a customer
  moves or renames itself, or we change a price, invoices already issued still show the old details.
- A mistake on an issued invoice is corrected with a credit note and a new invoice, never by editing it.
- Invoice numbers are consecutive, without gaps. The app takes the next number inside the same operation that
  issues the invoice (one user at a time; see the README).
- Customers can look up any invoice from the last seven years and we must be able to print it again exactly
  as issued.

That is why `Invoice` copies `bill_to_name`, `bill_to_address` and `vat_number` from the customer when it is
issued, and why each line keeps its own `description` and `unit_price_cents`. The `Customer` row always holds the current
details, which is what new invoices and the order screens use.
