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
    """Employee ids who approve a claim from employee_id, in order, starting with their manager.

    Follows solid reporting lines only (dotted-line leads never sign). The chain stops at the
    first person of grade 7 or above, who is included as the last approver. If the chain comes
    back to someone already in it (or to the submitter) it stops there without repeating them;
    HR ops picks such claims up by hand.
    """
    rows = conn.execute(
        """
        WITH RECURSIVE chain(id, grade, depth, path) AS (
            SELECT e.id, e.grade, 1, ',' || ? || ',' || e.id || ','
            FROM reporting_line rl JOIN employee e ON e.id = rl.manager_id
            WHERE rl.employee_id = ? AND rl.kind = 'solid' AND e.id != ?
          UNION ALL
            SELECT e.id, e.grade, c.depth + 1, c.path || e.id || ','
            FROM chain c
            JOIN reporting_line rl ON rl.employee_id = c.id AND rl.kind = 'solid'
            JOIN employee e ON e.id = rl.manager_id
            WHERE c.grade < 7 AND instr(c.path, ',' || e.id || ',') = 0
        )
        SELECT id FROM chain ORDER BY depth
        """,
        (employee_id, employee_id, employee_id),
    ).fetchall()
    return [r[0] for r in rows]
