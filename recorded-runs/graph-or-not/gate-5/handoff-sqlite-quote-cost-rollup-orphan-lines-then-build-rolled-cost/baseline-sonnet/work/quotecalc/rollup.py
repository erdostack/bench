"""Rolled-up unit cost of an item."""

# Every item id reachable below the quoted one. UNION (not UNION ALL) drops repeats, so a
# subassembly used on many paths is visited once and a cycle in bad data cannot loop.
# Only made items are expanded; a bought item is a leaf. Uses the bom_line primary key.
REACHABLE_SQL = """
WITH RECURSIVE reach(id) AS (
    SELECT :root
    UNION
    SELECT b.component_id
      FROM reach r
      JOIN item p ON p.id = r.id AND p.kind = 'made'
      JOIN bom_line b ON b.parent_id = r.id
)
SELECT r.id, i.kind, i.std_cost, i.labour_cost
  FROM reach r LEFT JOIN item i ON i.id = r.id
"""


def rolled_cost(conn, item_id):
    """Rolled-up unit cost, or None when anything anywhere under the item is missing.

    Finance's rule: a component id with no row in item (or a node with no cost) makes every
    assembly above it incomplete, so the answer is None, never a partial total.
    """
    nodes = {i: (kind, std, lab) for i, kind, std, lab in conn.execute(REACHABLE_SQL, {"root": item_id})}
    memo, active = {}, set()

    def cost(i):
        if i in memo:
            return memo[i]
        if i in active:                       # cycle: no sensible cost
            return None
        kind, std, lab = nodes[i]
        if kind is None:                      # dangling reference
            memo[i] = None
        elif kind == "bought":
            memo[i] = std
        else:
            active.add(i)
            total = lab
            for comp, qty in conn.execute("SELECT component_id, qty FROM bom_line WHERE parent_id = ?", (i,)):
                sub = cost(comp)
                total = None if total is None or sub is None else total + qty * sub
            active.discard(i)
            memo[i] = total
        return memo[i]

    return cost(item_id) if item_id in nodes else None
