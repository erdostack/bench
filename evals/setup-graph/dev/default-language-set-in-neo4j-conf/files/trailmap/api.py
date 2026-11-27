from fastapi import FastAPI

from . import graph

app = FastAPI(title="trailmap")


@app.get("/huts/{hut}/within-a-day")
def within_a_day(hut: str, hours: float = 7.0):
    return graph.read(graph.saved("huts_within_a_day"), start=hut, budget=hours * 60)


@app.get("/huts/{hut}/loops")
def loops(hut: str, days: int = 3):
    return graph.read(graph.saved("loops_from"), start=hut, days=days)
