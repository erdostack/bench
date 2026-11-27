from fastapi import FastAPI, HTTPException

from . import loans, makers

app = FastAPI(title="curio")


@app.get("/objects/on-loan")
def objects_on_loan():
    return loans.on_loan()


@app.get("/objects/{accession}/provenance")
def object_provenance(accession: str):
    chain = makers.provenance(accession)
    if not chain:
        raise HTTPException(status_code=404, detail="unknown accession number")
    return chain


@app.get("/makers/{name}/network")
def maker_network(name: str, depth: int = 3):
    return makers.network(name, depth)
