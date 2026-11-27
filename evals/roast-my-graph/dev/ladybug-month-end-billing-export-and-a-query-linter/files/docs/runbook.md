# Month-end billing runbook

1. Wait for the meter-data system's "estimates written" message (first working day, 06:00).
2. Run `meters_without_reading` and `meters_without_owner` from billing/checks.cypher with this month's date.
   Both must return no rows. If either returns rows, stop and raise a ticket with meter data.
3. Run `python -m billing.export <month> out/<month>.csv` and compare the printed row count with the meter count
   on the meter-data dashboard. They must match.
4. Upload the file to billing.
