# pedalpool

A shared e-bike scheme for companies: an employer opens an account, its staff ride, and we invoice the
employer every month for the minutes ridden. LadybugDB, embedded in the billing service.

    db/schema.cypher      table definitions
    db/billing.cypher     what the billing run uses; each query has a `// name:` line
    billing/run.py        the monthly billing run (on the 2nd of each month, for the previous month)
    billing/periods.py    billing periods

## Billing rules

The invoice for a month covers every ride that ended in that month, from the 1st to the last day of the
month inclusive, and each ride is billed exactly once. The invoice shows the total minutes and the number of
rides, and has the list of those rides attached as a statement.

## Numbers

1,400 company accounts, 52,000 riders, about 610,000 rides a month (20,000 on an ordinary day; more on the
last working day of the month, when people ride to the end-of-month drinks).
