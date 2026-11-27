"""Runs every minute from the auth service's scheduler."""
from pathlib import Path

QUERY = (Path(__file__).resolve().parent.parent / "queries" / "expire_codes.cypher").read_text()


def expire_codes(driver):
    # One managed transaction on purpose: the ExpiryRun audit record and the deletes commit together,
    # or neither does (SEC-88).
    with driver.session(database="gatekeep") as session:
        session.execute_write(lambda tx: tx.run(QUERY).consume())
