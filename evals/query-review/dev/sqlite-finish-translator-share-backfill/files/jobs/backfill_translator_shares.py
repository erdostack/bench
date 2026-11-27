"""Backfill translator shares: an earns_on edge for every translator contract in contract_import.
Translator contracts were kept only in the rights system until now (ticket ROY-77)."""
import logging

BATCH = 500
log = logging.getLogger("backfill_translator_shares")


def run(conn):
    rows = conn.execute("SELECT contract_id, contributor_id, title_id, share_bp FROM contract_import "
                        "WHERE role = 'translator' ORDER BY contract_id").fetchall()
    total = (len(rows) + BATCH - 1) // BATCH
    for k in range(total):
        chunk = rows[k * BATCH:(k + 1) * BATCH]
        with conn:
            conn.executemany("INSERT INTO edges (src, dst, kind, role, share_bp, contract_id) "
                             "VALUES (?, ?, 'earns_on', 'translator', ?, ?)",
                             [(c, t, s, cid) for cid, c, t, s in chunk])
        log.info("committed batch %d/%d", k + 1, total)
    return len(rows)
