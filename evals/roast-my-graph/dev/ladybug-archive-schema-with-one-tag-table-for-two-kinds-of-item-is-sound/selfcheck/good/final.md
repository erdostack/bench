Honestly: he's not right, and there's nothing critical or high to put on that list.

- "No indexes": in LadybugDB every node table has to have a primary key, and that key is indexed. All four tables have one, and every desk query starts from a key (tag slug, staff number, item id) and walks from there. The one exception, looking an article up by its slug, is a deliberate scan that docs/decisions.md says the desk accepted.
- "No constraints": the primary keys are the uniqueness constraints.
- "A relationship table that points at two different things": TaggedWith and MadeBy each list two FROM/TO pairs, which LadybugDB supports, and it's the sensible choice when articles and episodes share one tag vocabulary.

The list I'd bring him has three low or medium items, in docs/graph/ROAST.md and findings.json.
