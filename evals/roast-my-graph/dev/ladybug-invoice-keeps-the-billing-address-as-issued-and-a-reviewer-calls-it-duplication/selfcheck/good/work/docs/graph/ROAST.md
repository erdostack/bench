# Roast: crumb invoicing

Read against the invoicing rules in docs/invoicing.md.

## Findings

### 1. Invoice.bill_to_address (low)

**Problem.** Questioned as duplication. It is the address as invoiced, which the rules require to stay as issued; Customer.billing_address is the current one and update_customer changes it in place. Different facts, both needed.

**Fix.** Keep it, and give delivery notes the same kind of copy when you add them.

### 2. issue_invoice (medium)

**Problem.** The invoice and its lines are written by separate statements (issue_invoice, then add_line per line). If the app stops in between, an invoice number exists with no or some lines, and the numbering rule forbids just deleting it.

**Fix.** Run issue_invoice and its add_line calls in one transaction in the app.

### 3. next_invoice_number (low)

**Problem.** max + 1 in its own statement is only safe with one writer. That is the case today (one process, one user).

**Fix.** Keep it while that holds; if a second writer ever appears, take the number in the same transaction as issue_invoice.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
