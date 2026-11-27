Position: keep

Yusuf, we moved the grouping to networkx because the SQL loop took about 3 hours against a 2 hour window, while
networkx did it in 20 minutes using 8 GB. Recursive CTEs will not be faster than that.
