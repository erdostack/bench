"""Trial balance report."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def own_balance(conn, account_id, period):
    return conn.execute((SQL / "balance.sql").read_text(), {"account_id": account_id, "period": period}).fetchone()[0]


# TODO: the trial balance needs a subtotal per account that includes every account below it.
