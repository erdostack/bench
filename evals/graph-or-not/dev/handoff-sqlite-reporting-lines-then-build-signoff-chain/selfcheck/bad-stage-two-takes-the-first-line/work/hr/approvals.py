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


DIRECTOR_GRADE = 7   # Finance: the first person at grade 7 or above is the last approver (docs/graph/DECISION.md)


def line_manager(conn, employee_id):
    row = conn.execute("SELECT manager_id FROM reporting_line WHERE employee_id = ?",
                       (employee_id,)).fetchone()
    return row[0] if row else None


def signoff_chain(conn, employee_id):
    """Approvers of a claim submitted by employee_id, in order, starting with their line manager.

    Solid lines only. Stops at the first person at grade 7 or above (included), and when the chain comes back to
    someone already in it or to the submitter (the export has loops; HR ops takes those)."""
    chain, seen = [], {employee_id}
    current = line_manager(conn, employee_id)
    while current is not None and current not in seen:
        chain.append(current)
        seen.add(current)
        row = employee(conn, current)
        if row is None or row[2] >= DIRECTOR_GRADE:
            break
        current = line_manager(conn, current)
    return chain
