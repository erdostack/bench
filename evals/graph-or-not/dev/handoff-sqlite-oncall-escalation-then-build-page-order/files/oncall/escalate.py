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


# TODO: the alert detail page should show the escalation path the alert will take if nobody acks
#       (which policies, in order), so people stop guessing who gets woken up next.
