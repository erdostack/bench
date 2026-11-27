planning/requirements.py: gross_requirements builds a DiGraph from bom_line and walks down, multiplying each
line by qty_per x 1.04 (scrap rule in docs/graph/DECISION.md), summing bought-in parts.
