# Schema decisions

1. **One tag table for both kinds of item.** Articles and episodes are tagged from the same vocabulary, and
   the desk almost always wants both ("everything we have on the bypass"). `TaggedWith` and `MadeBy` are each
   one relationship table with two `FROM ... TO ...` pairs, one per kind of item, instead of four tables.
   Queries that want one kind say so in the pattern.
2. **Articles and episodes stay separate node tables.** They share little beyond a title and a date
   (episodes have a duration and an audio file, articles a word count and a section), and LadybugDB tables
   have fixed columns, so one table would be half empty.
3. **Keys.** Every node table has a primary key: the CMS id for items (`a-1234567`, `e-8812`), the staff
   number for people, the tag slug for tags. Lookups by slug use the `slug` column on Article, which the desk
   tool only uses when someone pastes a URL; it is a scan of one table and takes about a second, which the
   desk is happy with.
4. **No separate indexes.** LadybugDB indexes the primary key of every node table; every other access is a
   traversal from a node found by its key.
