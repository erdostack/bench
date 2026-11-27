from fastapi import FastAPI

from .sql import downstream_columns

app = FastAPI()


@app.get("/impact/{column_id}")
def impact(column_id: int):
    return downstream_columns(column_id)
