"""Who approves what. conn is a sqlite3 connection to the HR directory export (db/schema.sql)."""


def employee(conn, employee_id):
    """(id, name, grade, department) or None."""
    return conn.execute("SELECT id, name, grade, department FROM employee WHERE id = ?", (employee_id,)).fetchone()


def reporting_lines(conn, employee_id):
    """[(manager_id, kind), ...] for one employee, as the HR app exported them."""
    return conn.execute("SELECT manager_id, kind FROM reporting_line WHERE employee_id = ?", (employee_id,)).fetchall()


def can_approve_amount(grade, amount_eur):
    """Spending authority by grade (finance policy FP-12)."""
    limits = {1: 0, 2: 0, 3: 500, 4: 1_000, 5: 2_500, 6: 5_000}
    return grade >= 7 or amount_eur <= limits.get(grade, 0)


SENIOR_GRADE = 7  # agreed with Finance: the chain ends at the first approver of this grade or above


def signoff_chain(conn, employee_id):
    """Approvers in order, going up from the submitter's own solid-line manager.

    Returns (approvers, outcome). approvers is a list of (id, name, grade, department).
      outcome "complete":  the last approver is grade 7 or above.
      outcome "loop":      the chain came back to someone already in it, the submitter included. The
                           approvers found so far are returned and HR ops picks the claim up by hand.
      outcome "no_senior": the solid-line chain ran out before reaching grade 7. Also for HR ops.
    Returns None if employee_id is not in the export.

    Dotted lines are never followed. The schema allows one solid line per employee, so this is a walk
    up a single path, at most about 12 steps; no graph tooling is needed.
    """
    if employee(conn, employee_id) is None:
        return None
    seen = {employee_id}
    approvers = []
    current = employee_id
    while True:
        solid = [m for m, kind in reporting_lines(conn, current) if kind == "solid"]
        if not solid:
            return approvers, "no_senior"
        manager_id = solid[0]
        if manager_id in seen:
            return approvers, "loop"
        seen.add(manager_id)
        manager = employee(conn, manager_id)
        approvers.append(manager)
        if manager[2] >= SENIOR_GRADE:
            return approvers, "complete"
        current = manager_id
