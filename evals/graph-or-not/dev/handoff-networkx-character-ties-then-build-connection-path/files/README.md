# companion

The reading-companion site for our annotated edition of *Les Misérables*: character pages, who appears with whom,
chapter notes. One small VM, Flask, SQLite.

- Python 3.12, `requirements.txt`.
- Character and tie data are in `data/` (committed). `python scripts/load.py` builds `var/companion.db` from them
  (not committed). Tables are in `db/schema.sql`.
- `flask --app companion.app run` for local work.

The character network is the co-appearance network of the novel (Knuth's *Stanford GraphBase* compilation, as
shipped with networkx as `les_miserables_graph`): a tie means two characters appear in the same chapter, and its
weight is the number of chapters they share.

## Layout

    data/characters.csv     id,name
    data/ties.csv           char_a,char_b,weight
    db/schema.sql           tables
    scripts/load.py         csv -> var/companion.db
    companion/app.py        routes
    companion/stats.py      "most connected characters" box
