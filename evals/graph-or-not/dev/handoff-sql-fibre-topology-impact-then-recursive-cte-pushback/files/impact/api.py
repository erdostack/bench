import psycopg
from fastapi import FastAPI

from impact.walk import impact

app = FastAPI()
DSN = "dbname=inventory"


@app.get("/impact/span/{link_id}")
def span_impact(link_id: int):
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        return {"link_id": link_id, "devices": impact(cur, link_id)}
