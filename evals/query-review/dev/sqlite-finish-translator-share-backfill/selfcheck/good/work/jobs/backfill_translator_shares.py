"""Backfill translator shares: an earns_on edge for every translator contract in contract_import.
Translator contracts were kept only in the rights system until now (ticket ROY-77).
Safe to rerun: a contract that already has its edge is skipped (keyed on contract_id)."""
import logging

BATCH = 500
log = logging.getLogger("backfill_translator_shares")


def run(conn):
    added = 0
    while True:
        with conn:
            n = conn.execute(
                "INSERT INTO edges (src, dst, kind, role, share_bp, contract_id) "
                "SELECT c.contributor_id, c.title_id, 'earns_on', 'translator', c.share_bp, c.contract_id "
                "FROM contract_import c WHERE c.role = 'translator' AND NOT EXISTS "
                "(SELECT 1 FROM edges e WHERE e.contract_id = c.contract_id) "
                "ORDER BY c.contract_id LIMIT ?", (BATCH,)).rowcount
        added += n
        log.info("committed %d", n)
        if n == 0:
            return added
