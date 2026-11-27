"""The capacity planning run."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def changed_components(conn, run_id):
    return [r[0] for r in conn.execute("SELECT component_id FROM component_change WHERE run_id = ?", (run_id,))]


def where_used(conn, component_id):
    return [r[0] for r in conn.execute((SQL / "where_used.sql").read_text(), {"component_id": component_id})]


def affected_assemblies(conn, run_id):
    """Union of the where-used of every changed component, one set-based query, each assembly once."""
    return [r[0] for r in conn.execute((SQL / "where_used_batch.sql").read_text(), {"run_id": run_id})]


def run(conn, run_id, retime):
    # retime() takes only the assembly, so one call per distinct assembly is enough; the per-component
    # loop re-walked shared ancestors and called retime() repeatedly on the same assembly.
    for assembly in affected_assemblies(conn, run_id):
        retime(assembly)
