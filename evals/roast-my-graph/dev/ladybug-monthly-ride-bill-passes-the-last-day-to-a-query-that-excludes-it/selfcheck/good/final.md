The two queries disagree about the last day of the month, and the one that sets the bill is the one that's wrong.

month_period gives the first and the last day of the month, and both queries get those same two dates. The statement includes the last day (<=), but account_totals, which sets the minutes and the amount, uses < and so leaves out every ride that ended on the last day. Next month's run starts from the 1st, so those rides are never billed at all. That's your customers' "list doesn't match the total", and it's lost revenue every month, more than a thirtieth because month-end is busy.

Fix: <= in account_totals (or pass the 1st of the next month as an exclusive end and use < in both). Details in docs/graph/ROAST.md and findings.json.
