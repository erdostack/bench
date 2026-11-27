"""bandtree-ask <file.cypher> [name=value ...]: run one saved query read-only and print the rows."""
from pathlib import Path

import click

from . import store


@click.command()
@click.argument("query_file", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("params", nargs=-1)
def main(query_file: Path, params: tuple[str, ...]) -> None:
    values = dict(item.split("=", 1) for item in params)
    result = store.connect().execute(query_file.read_text(), values)
    click.echo("\t".join(result.get_column_names()))
    while result.has_next():
        click.echo("\t".join(str(value) for value in result.get_next()))


if __name__ == "__main__":
    main()
