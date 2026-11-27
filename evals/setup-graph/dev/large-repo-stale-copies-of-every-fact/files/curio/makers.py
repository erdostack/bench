from . import graph


def network(maker: str, depth: int = 3) -> list[dict]:
    """Teachers and pupils of a maker, out to `depth` steps."""
    if not 1 <= depth <= 6:
        raise ValueError("depth must be between 1 and 6")
    return graph.read(graph.saved("maker_network"), maker=maker, depth=depth)


def provenance(accession: str) -> list[dict]:
    return graph.read(graph.saved("provenance_chain"), accession=accession)
