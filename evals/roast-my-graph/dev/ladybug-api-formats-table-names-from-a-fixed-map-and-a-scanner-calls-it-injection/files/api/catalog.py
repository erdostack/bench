"""What the browse API exposes. Only names in these two maps ever reach a query string.

Table, column and relationship names cannot be passed as query parameters (parameters stand for values), so
browse.py writes them into the query text. It only ever takes them from the maps below, never from the
request: the request picks a key, and an unknown key is a 404 before any query is built.
"""

# url name -> (node table, key column, columns shown in lists)
TABLES = {
    "cultivars": ("Cultivar", "code", ("code", "name", "species", "released")),
    "trials": ("Trial", "id", ("id", "season", "design")),
    "sites": ("Site", "code", ("code", "name", "soil")),
    "people": ("Person", "id", ("id", "name", "team")),
}

# url name -> (from table, relationship table, to table)
LINKS = {
    "grown-in": ("Cultivar", "GrownIn", "Trial"),
    "held-at": ("Trial", "HeldAt", "Site"),
    "run-by": ("Trial", "RunBy", "Person"),
    "parents": ("Cultivar", "BredFrom", "Cultivar"),
}
