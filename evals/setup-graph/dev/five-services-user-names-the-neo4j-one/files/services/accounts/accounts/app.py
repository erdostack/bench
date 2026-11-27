from fastapi import FastAPI

from . import store

app = FastAPI(title="accounts")


@app.get("/customers/{customer_id}/invoices")
def invoices(customer_id: int):
    return store.invoices_for(customer_id)
