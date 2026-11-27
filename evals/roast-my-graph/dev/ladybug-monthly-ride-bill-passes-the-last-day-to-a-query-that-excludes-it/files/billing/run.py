"""Monthly billing run. See README.md for the rules."""
from datetime import date

import ladybug

from .periods import previous_month

QUERIES_FILE = "db/billing.cypher"


def load_queries(path=QUERIES_FILE):
    text = open(path, encoding="utf-8").read()
    out = {}
    for block in text.split("// name: ")[1:]:
        name, _, body = block.partition("\n")
        out[name.strip()] = body.strip().rstrip(";")
    return out


def bill_month(conn, today=None):
    first_day, last_day = previous_month(today or date.today())
    q = load_queries()
    invoices = []
    for account_id, company, rate in conn.execute(q["billable_accounts"]).get_all():
        params = {"account": account_id, "first_day": first_day, "last_day": last_day}
        rides, minutes = conn.execute(q["account_totals"], params).get_all()[0]
        if not rides:
            continue
        statement = conn.execute(q["account_statement"], params).get_all()
        invoices.append({
            "account": account_id,
            "company": company,
            "period": (first_day, last_day),
            "rides": rides,
            "minutes": minutes,
            "amount_cents": minutes * rate,
            "statement": statement,
        })
    return invoices
