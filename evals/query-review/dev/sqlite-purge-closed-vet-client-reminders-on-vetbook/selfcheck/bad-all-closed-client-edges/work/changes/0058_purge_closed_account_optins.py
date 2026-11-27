"""0058 DPO audit: closed accounts keep nothing linked to them."""


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(
                "DELETE FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN nodes c ON c.id = e.src "
                "WHERE c.kind = 'client' AND c.status = 'closed' LIMIT 500)").rowcount
        if not n:
            return removed
        removed += n
