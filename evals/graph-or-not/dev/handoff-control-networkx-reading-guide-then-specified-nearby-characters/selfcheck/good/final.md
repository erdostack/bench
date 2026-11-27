Added guide/nearby.py: characters_within(conn, name, steps) builds the tie graph and returns everyone within
`steps` ties of the character (a breadth-first search with a cutoff), the character itself left out.
