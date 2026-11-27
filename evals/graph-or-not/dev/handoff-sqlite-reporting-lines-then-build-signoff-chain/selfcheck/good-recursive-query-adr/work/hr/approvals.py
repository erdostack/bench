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


SIGNOFF_SQL = """
WITH RECURSIVE up(id, grade, step, path) AS (
    SELECT e.id, e.grade, 1, ',' || :start || ',' || e.id || ','
    FROM reporting_line r JOIN employee e ON e.id = r.manager_id
    WHERE r.employee_id = :start AND r.kind = 'solid' AND r.manager_id <> :start
    UNION ALL
    SELECT e.id, e.grade, up.step + 1, up.path || e.id || ','
    FROM up
    JOIN reporting_line r ON r.employee_id = up.id AND r.kind = 'solid'
    JOIN employee e ON e.id = r.manager_id
    WHERE up.grade < 7                                    -- grade 7 or above is the last approver (ADR 0003)
      AND instr(up.path, ',' || e.id || ',') = 0          -- the export has loops
)
SELECT id FROM up ORDER BY step
"""


def signoff_chain(conn, employee_id):
    """Approvers in order, per ADR 0003."""
    return [r[0] for r in conn.execute(SIGNOFF_SQL, {"start": employee_id})]
