# wordroots

Where words come from, as a graph: a word, the word it was borrowed or derived from, and so on back. Good for
questions like "which English words go back to the same Old Norse root?"

The data is a hand-made sample (see `data/`), loaded into an embedded LadybugDB database with the `lbug` package.
No database server is involved; the database is the `var/wordroots.lbug` directory.

    pnpm install
    pnpm load
    pnpm ask queries/ancestors_of.cypher word=window

`pnpm ask` opens the database read-only and prints the rows of one saved query.
