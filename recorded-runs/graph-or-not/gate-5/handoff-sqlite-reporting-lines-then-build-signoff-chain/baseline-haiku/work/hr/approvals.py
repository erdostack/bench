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


def signoff_chain(conn, employee_id):
    """Ids of the people who approve a claim from employee_id, in order, starting with their solid-line manager.

    Walks up 'solid' reporting lines only; 'dotted' leads do not sign off. The submitter is not included.
    Stops at the top of the line or if a cycle in the export would otherwise loop forever.
    """
    chain = []
    seen = {employee_id}
    current = employee_id
    while True:
        row = conn.execute(
            "SELECT manager_id FROM reporting_line WHERE employee_id = ? AND kind = 'solid'", (current,)
        ).fetchone()
        if row is None:
            break
        manager = row[0]
        if manager in seen:
            break
        chain.append(manager)
        seen.add(manager)
        current = manager
    return chain


# TODO: sign-off chain for expense claims and leave requests: the people who approve, in order, going up
#       from the person who submitted it. The approval page should show it before the claim is sent.
