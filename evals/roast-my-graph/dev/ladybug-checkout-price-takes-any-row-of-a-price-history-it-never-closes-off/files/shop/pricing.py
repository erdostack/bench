"""Prices for checkout and the admin pages. conn is a ladybug.Connection."""
from datetime import date, timedelta

from .queries import Q  # the statements of db/prices.cypher, by name


class NoPrice(Exception):
    pass


def price_at_checkout(conn, school, sku, today=None):
    rows = conn.execute(Q["price_at_checkout"],
                        {"sku": sku, "school": school, "today": today or date.today()}).get_all()
    if not rows:
        raise NoPrice(sku)
    return rows[0][0]


def set_price(conn, sku, list_code, price_cents, starts):
    """Close the current price and add the new one from `starts`. See docs/prices.md."""
    conn.execute("BEGIN TRANSACTION")
    try:
        conn.execute(Q["close_current_price"],
                     {"sku": sku, "list": list_code, "day_before": starts - timedelta(days=1)})
        conn.execute(Q["add_price"],
                     {"sku": sku, "list": list_code, "price_cents": price_cents, "from": starts})
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def export_list(conn, list_code, day):
    return conn.execute(Q["list_export"], {"list": list_code, "day": day}).get_all()
