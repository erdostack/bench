"""Which judge marks which project. Rules in docs/graph/DECISION.md."""
import networkx as nx

MAX_PER_JUDGE = 5


def eligible_judges(conn, project_id):
    """Judges who cover the project's category and are not from the project's school."""
    rows = conn.execute(
        "SELECT j.id FROM judge j JOIN judge_category c ON c.judge_id = j.id "
        "JOIN project p ON p.category = c.category "
        "WHERE p.id = ? AND j.school <> p.school ORDER BY j.id", (project_id,))
    return [r[0] for r in rows]


def assign(conn):
    """Return {project_id: judge_id}, judging as many projects as the cap allows."""
    g = nx.DiGraph()
    for (pid,) in conn.execute("SELECT id FROM project").fetchall():
        g.add_edge("source", ("p", pid), capacity=1)
        for jid in eligible_judges(conn, pid):
            g.add_edge(("p", pid), ("j", jid), capacity=1)
    for (jid,) in conn.execute("SELECT id FROM judge"):
        g.add_edge(("j", jid), "sink", capacity=MAX_PER_JUDGE)
    _, flow = nx.maximum_flow(g, "source", "sink")
    out = {}
    for node, targets in flow.items():
        if isinstance(node, tuple) and node[0] == "p":
            for target, f in targets.items():
                if f > 0.5:
                    out[node[1]] = target[1]
    return out
