Added planning/requirements.py. gross_requirements(conn, item_id, qty) runs one WITH RECURSIVE query down
bom_line, multiplies each line's qty_per by 1.04 (the 4% scrap per line from docs/graph/DECISION.md, so it
compounds per level), and sums per bought-in part. Returns {item_id: qty} rounded to 3 decimals.
