Your architect is right. Text paths are an anti-pattern: they break, they scan, and moves rewrite the table.
Replace them with parent_id before the other districts join.
