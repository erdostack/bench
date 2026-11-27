Position: keep

With a depth column UNION can't remove repeats on a loop, because every lap has a different depth, and a
cap might cut off deeply nested lists. The path guard is the standard way to handle cycles in a recursive
query, so we should keep it.
