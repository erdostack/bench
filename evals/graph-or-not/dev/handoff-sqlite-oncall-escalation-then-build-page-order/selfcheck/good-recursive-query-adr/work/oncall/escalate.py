"""What happens to an alert that nobody acks. conn is a sqlite3 connection to the pager config."""


def targets(conn, policy_id):
    """People paged when an alert reaches policy_id."""
    rows = conn.execute("SELECT person_id FROM policy_target WHERE policy_id = ? ORDER BY person_id", (policy_id,))
    return [r[0] for r in rows]


def next_policy(conn, policy_id):
    """The policy an unacked alert moves to from policy_id, or None."""
    row = conn.execute("SELECT escalates_to FROM escalation_policy WHERE id = ?", (policy_id,)).fetchone()
    return row[0] if row else None


def ack_timeout(conn, policy_id):
    row = conn.execute("SELECT ack_timeout_s FROM escalation_policy WHERE id = ?", (policy_id,)).fetchone()
    return row[0] if row else None


PAGE_ORDER_SQL = """
WITH RECURSIVE walk(id, step, path) AS (
    SELECT id, 1, ',' || id || ',' FROM escalation_policy WHERE id = :start
    UNION ALL
    SELECT p.escalates_to, w.step + 1, w.path || p.escalates_to || ','
    FROM walk AS w
    JOIN escalation_policy AS p ON p.id = w.id
    WHERE p.escalates_to IS NOT NULL
      AND w.step < 5                                              -- at most 4 escalations
      AND instr(w.path, ',' || p.escalates_to || ',') = 0         -- never page a policy twice
)
SELECT id FROM walk ORDER BY step
"""


def page_order(conn, policy_id):
    """Escalation path of an unacked alert, per ADR 0004."""
    return [r[0] for r in conn.execute(PAGE_ORDER_SQL, {"start": policy_id})]
