There is one real problem and it is at the bottom of everything else: the graph thinks there is exactly one room 101 in the whole group.

schema.cypher makes Room.number unique across all rooms, and load_rooms merges a Room on the number alone. But every hotel numbers its own rooms (README), and the sample export has a 101 in all four hotels. So those four rooms are one node, attached to four hotels, carrying whichever hotel's beds and rate class loaded last. Book 101 in Amsterdam and 101 disappears from the search in Lisbon, Prague and Vienna for those nights.

The fix is to identify a room by hotel and number together. Details and three smaller notes are in docs/graph/ROAST.md and findings.json.
