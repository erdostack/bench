# Roast: coopmarket board reports

Checked each report for what one row means before it is summed.

## Findings

### 1. region_revenue (critical)

**Problem.** The MATCH continues from each order to its Contains lines, so the rows are order lines, not orders. sum(o.total_cents) therefore adds an order's total once per line: an order with n lines counts n times. count(DISTINCT o) and sum(c.qty) are right, which hides it. With 4.3 lines per order on average, and more in the town shops, revenue is overstated roughly four times overall and more for town regions, and the bonus pool is split on these numbers.

**Fix.** Sum per line: RETURN ..., count(DISTINCT o) AS orders, sum(c.qty) AS units, sum(c.line_cents) AS revenue_cents. If the till total must be used, aggregate per order first: WITH r, o, sum(c.qty) AS units RETURN r.code, count(o) AS orders, sum(units) AS units, sum(o.total_cents) AS revenue_cents. Then recompute this year's bonus split.

### 2. previous_month (low)

**Problem.** Works, but last_month_end is the first day of this month under a misleading name (it is used as an exclusive end, which is right for the < $to in the queries).

**Fix.** Rename it to end_exclusive.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
