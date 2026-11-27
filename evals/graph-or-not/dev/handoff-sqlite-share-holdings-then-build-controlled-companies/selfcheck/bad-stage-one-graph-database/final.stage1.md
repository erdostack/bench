Decision: graph-database

Neha is right that ownership is a graph, and with 3.4M holdings, loops and chains of 9 companies the recursive SQL
will be hard to maintain. A graph database makes the control chain a variable-length pattern match, and it will
pay off as compliance asks for more ownership questions. Start with a nightly load from the registry feed.
