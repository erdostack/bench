"""Monthly invoice run. One invoice per account with usage in the period."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def run(conn, period):
    usage = conn.execute((SQL / "usage_by_account.sql").read_text(), {"period": period}).fetchall()
    # TODO: consolidated invoicing. Group charges under the paying account instead of one invoice each.
    return [{"account_id": a, "lines": [amount]} for a, amount in usage]
