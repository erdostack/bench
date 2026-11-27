from pathlib import Path

SQL = (Path(__file__).resolve().parents[1] / "sql" / "ubo.sql").read_text().replace(":company_id", "%(company_id)s")


def owners(cur, company_id, threshold_pct=25):
    cur.execute(SQL, {"company_id": company_id})
    return [(holder, float(pct)) for holder, pct in cur.fetchall() if pct >= threshold_pct]
