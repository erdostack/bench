"""Board pack, run on the 1st of each month for the month before."""
from datetime import date

import ladybug

REPORTS = ["region_revenue", "shop_orders", "top_products", "category_mix"]


def load_reports(path="db/reports.cypher"):
    text = open(path, encoding="utf-8").read()
    out = {}
    for block in text.split("// name: ")[1:]:
        name, _, body = block.partition("\n")
        out[name.strip()] = body.strip().rstrip(";")
    return out


def previous_month(today):
    first_this = today.replace(day=1)
    last_month_end = first_this
    year, month = (first_this.year, first_this.month - 1) if first_this.month > 1 else (first_this.year - 1, 12)
    return date(year, month, 1), last_month_end


def main(today=None):
    start, end = previous_month(today or date.today())
    conn = ladybug.Connection(ladybug.Database("/srv/coop/coop.lbdb", read_only=True))
    queries = load_reports()
    pack = {}
    for name in REPORTS:
        pack[name] = conn.execute(queries[name], {"from": start, "to": end}).get_all()
    return pack
