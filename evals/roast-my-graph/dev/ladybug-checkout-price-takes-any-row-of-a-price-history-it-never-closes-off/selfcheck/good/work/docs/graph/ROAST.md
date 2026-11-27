# Roast: threadline pricing

Read with docs/prices.md: prices are a history, never edited in place.

## Findings

### 1. price_at_checkout (critical)

**Problem.** The filter is valid_from <= $today only. Closed rows (valid_to set in the past) also pass it, so for a product with five price rows the MATCH returns up to five prices, and LIMIT 1 with no ORDER BY returns whichever row comes first. Nothing makes that the current price, so checkout can charge any earlier year's price. With three to eight rows per product per list, most basket lines are exposed. It looks right on a test database where each product has one price.

**Fix.** Select the row that is valid today: WHERE p.sku = $sku AND s.code = $school AND x.valid_from <= $today AND (x.valid_to IS NULL OR x.valid_to >= $today), the same condition as list_export. Add a test with a closed row and a current row.

### 2. set_price (medium)

**Problem.** If a future price is already waiting (agreed in June for 1 August) and another change comes in before August, close_current_price closes the row with no valid_to, which is the future one, before it ever starts, while today's row keeps running to its end date. The new row then overlaps today's, and the agreed August price is lost.

**Fix.** When adding a price, close every row whose period overlaps the new one, or refuse a new price while a future one is pending.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
