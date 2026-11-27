Found why the sync doesn't finish. Every statement in the loader looks artworks up by accession number, and the schema has nothing on that property: the unique rule is on catalogue_id, which nothing searches by. So each of 1.9 million rows makes the database look through every artwork, three times over, and the public artwork page does the same per view. With four workers and no uniqueness rule you can also get the same artwork twice. One constraint on Artwork.accession_no fixes all of it (check for existing doubles first). Rated critical.

That's a roast of the schema, not of your junior: this is an easy thing to miss, since each file looks fine on its own, and I'd rather not pile on a person.

docs/graph/ROAST.md and findings.json have the details.
