Not warranted. The topic page is already an index lookup: tree.py binds the whole pattern (path + '%') as one
parameter, and topic.path is COLLATE NOCASE, which is what SQLite needs to serve a LIKE prefix from the index.
The query plan on kb.db is a range search on the path index, not a scan. Skip the closure table; just don't
change the query to concatenate the '%' in SQL, which would lose the index.
