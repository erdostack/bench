# Roast: galleria graph

"How hard can a loader be?" Hard enough, apparently, to defeat someone who has never met an index. Your junior constrained the one property nobody reads, which is the database equivalent of locking the bathroom window and leaving the front door open. Tell them a career in interpretive dance is still an option.

## Findings

### 1. Artwork.accession_no (critical)

**Problem.** Everything finds an artwork by its accession number: load_artworks, load_attributions, load_loans and the public artwork_page. Nothing in schema.cypher covers that property. The uniqueness rule for Artwork is on catalogue_id, which the loader only writes and nobody ever searches by. So for each of the 1.9 million rows in the export the database has to look through all 1.9 million artworks to see whether this one is already there, and it does that three times a night; that is why the sync is still running when the doors open. Every public page view does the same search once. And because four workers run at the same time and nothing says an accession number must be unique, two of them can each decide an artwork is missing and both create it.

**Fix.** CREATE CONSTRAINT artwork_accession_no IF NOT EXISTS FOR (a:Artwork) REQUIRE a.accession_no IS UNIQUE; Before creating it, check for artworks that already share an accession number (the parallel workers may have made some) and merge them. Keep or drop the catalogue_id constraint as you like; it is harmless but it is not the one the loader needs.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
