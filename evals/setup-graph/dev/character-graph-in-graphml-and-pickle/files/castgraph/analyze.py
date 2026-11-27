"""python -m castgraph.analyze <command>: the questions the study asks of the graph."""
import click
import networkx as nx

from .io import load


@click.group()
def main():
    """castgraph"""


@main.command()
def summary():
    graph = load()
    click.echo(f"{graph.number_of_nodes()} characters, {graph.number_of_edges()} co-occurrences, "
               f"{nx.number_connected_components(graph)} component(s)")


@main.command()
@click.option("--top", default=10, show_default=True)
def brokers(top: int):
    """Characters that sit on the most shortest paths between others."""
    scores = nx.betweenness_centrality(load(), weight=None)
    for name, score in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:top]:
        click.echo(f"{score:.3f}  {name}")


@main.command()
@click.argument("a")
@click.argument("b")
def between(a: str, b: str):
    """Shortest chain of co-occurrences from one character to another."""
    click.echo(" - ".join(nx.shortest_path(load(), a, b)))


if __name__ == "__main__":
    main()
