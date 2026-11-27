# pantrygraph

What can I cook with what is in the cupboard, and what is the one ingredient I am missing?

Recipes, ingredients and substitutions are stored in an embedded Kuzu database, so there is no server to run.
The database directory is created on first use (set `PANTRY_DB`, default `./var/pantry.kz`).

## Use

    pip install -r requirements.txt
    python -m pantry.cli load data/
    python -m pantry.cli query queries/almost_cookable.cypher

`requirements.txt` is generated from `requirements.in` with pip-compile; edit the `.in` file, not the output.
