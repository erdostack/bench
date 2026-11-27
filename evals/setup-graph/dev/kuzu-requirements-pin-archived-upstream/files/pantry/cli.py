"""Command line: load the CSVs, or run a saved query."""
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .db import connect

console = Console()


@click.group()
def main():
    """pantrygraph"""


@main.command()
@click.argument("data_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def load(data_dir: Path):
    """Create the tables and copy the CSV files in."""
    conn = connect(read_only=False)
    for statement in (Path(__file__).parent.parent / "schema" / "tables.cypher").read_text().split(";"):
        if statement.strip():
            conn.execute(statement)
    for table in ("Recipe", "Ingredient", "USES", "SWAPS_FOR"):
        conn.execute(f'COPY {table} FROM "{data_dir / (table.lower() + ".csv")}" (header=true)')


@main.command()
@click.argument("query_file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def query(query_file: Path):
    """Run one saved query read-only and print the rows."""
    result = connect().execute(query_file.read_text())
    table = Table(*result.get_column_names())
    while result.has_next():
        table.add_row(*[str(v) for v in result.get_next()])
    console.print(table)


if __name__ == "__main__":
    main()
