// name: next_invoice_number
MATCH (i:Invoice)
RETURN coalesce(max(i.number), 0) + 1 AS next_number;

// name: issue_invoice
MATCH (c:Customer)
WHERE c.id = $customer
CREATE (i:Invoice {number: $number, issued_on: $today, due_on: $due_on,
                   bill_to_name: c.name, bill_to_address: c.billing_address, vat_number: c.vat_number})
CREATE (i)-[:BilledTo]->(c);

// name: add_line
MATCH (i:Invoice), (p:Product)
WHERE i.number = $number AND p.code = $product
CREATE (i)-[:HasLine {line_no: $line_no, description: p.name, qty: $qty,
                      unit_price_cents: p.unit_price_cents}]->(p);

// name: print_invoice
MATCH (i:Invoice)-[l:HasLine]->(p:Product)
WHERE i.number = $number
RETURN i.number, i.issued_on, i.due_on, i.bill_to_name, i.bill_to_address, i.vat_number,
       l.line_no, p.code, l.description, l.qty, l.unit_price_cents, l.qty * l.unit_price_cents AS line_total_cents
ORDER BY l.line_no;

// name: customer_invoices
MATCH (i:Invoice)-[:BilledTo]->(c:Customer)
WHERE c.id = $customer
RETURN i.number, i.issued_on, i.due_on
ORDER BY i.number DESC;

// name: update_customer
MATCH (c:Customer)
WHERE c.id = $customer
SET c.name = $name, c.billing_address = $billing_address, c.vat_number = $vat_number;

// name: change_price
MATCH (p:Product)
WHERE p.code = $product
SET p.unit_price_cents = $unit_price_cents;

// name: rename_product
MATCH (p:Product)
WHERE p.code = $product
SET p.name = $name;
