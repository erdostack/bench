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


SIGNOFF_STOP_GRADE = 7   # the walk ends at the first approver of this grade or above
SIGNOFF_MAX_DEPTH = 12   # at most this many levels above the submitter

# Walks the solid line upward. Each employee has at most one solid manager (unique partial index),
# so this is a single path. A path string stops the walk before a manager already in the chain,
# including the submitter; dotted lines are never followed.
_SIGNOFF_SQL = """
WITH RECURSIVE chain(approver, grade, depth, path) AS (
  SELECT e.id, e.grade, 1, ',' || :emp || ',' || e.id || ','
  FROM reporting_line rl
  JOIN employee e ON e.id = rl.manager_id
  WHERE rl.employee_id = :emp AND rl.kind = 'solid' AND rl.manager_id <> :emp
  UNION ALL
  SELECT e.id, e.grade, c.depth + 1, c.path || e.id || ','
  FROM chain c
  JOIN reporting_line rl ON rl.employee_id = c.approver AND rl.kind = 'solid'
  JOIN employee e ON e.id = rl.manager_id
  WHERE c.grade < :stop_grade
    AND c.depth < :max_depth
    AND instr(c.path, ',' || e.id || ',') = 0
)
SELECT approver FROM chain ORDER BY depth
"""


def signoff_chain(conn, employee_id):
    """Ids of the people who approve a claim by employee_id, in order, starting with their solid manager.

    Stops at the first approver of grade 7 or above (that person is included), after 12 levels, or
    before a manager already in the chain (that person is not included). The submitter is never listed.
    A loop or a missing line ends the list early, and the return value does not say which ending it was.
    """
    rows = conn.execute(
        _SIGNOFF_SQL,
        {"emp": employee_id, "stop_grade": SIGNOFF_STOP_GRADE, "max_depth": SIGNOFF_MAX_DEPTH},
    ).fetchall()
    return [row[0] for row in rows]
