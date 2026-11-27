# Roast: buyline graph

Asked to be harsh. Reviewed against docs/retention.md and the README.

## Findings

### 1. retired_on (medium)

**Problem.** The 'not retired' condition is written by hand in category_page, supplier_catalogue and active_suppliers. All three have it today, but a new list statement could leave it out and show buyers things they can no longer order. That is the real part of the architect's concern; deleting retired products is not the answer, because ten years of orders point at them through LINE and TO.

**Fix.** Keep retired_on. Also add a :Retired label when retiring (SET p:Retired) so new statements can say WHERE NOT p:Retired, and add a test that runs every catalogue statement against a retired product and expects it not to appear.

### 2. spend_by_supplier (low)

**Problem.** Filters PurchaseOrder on placed_on without an index, so every order is read. 210,000 orders a few times a month is fine today.

**Fix.** If it ever runs from a screen, CREATE INDEX purchase_order_placed_on IF NOT EXISTS FOR (o:PurchaseOrder) ON (o.placed_on).

### 3. import_orders (low)

**Problem.** A row whose sku or supplier_code is not in the graph is dropped without a trace by the MATCH. The README says that cannot happen because products are created here first, so this is only a tripwire.

**Fix.** Have the import job compare the number of lines written with the number of rows sent and alert on a difference.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
