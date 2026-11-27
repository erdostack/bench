planning/requirements.py is in. It builds a DiGraph from bom_line and walks down from the item, multiplying
each edge's qty_per by 1.04, which is the scrap rule in docs/adr/0006-gross-requirements.md, and adds up the
bought-in parts.
