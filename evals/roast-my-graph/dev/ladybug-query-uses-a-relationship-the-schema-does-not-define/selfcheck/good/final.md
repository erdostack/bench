Review written to docs/graph/ROAST.md and findings.json.

Blocking (critical): genre_top uses a relationship named Reviewed. The schema has no Reviewed table; Reader to Book is Rated, which the other queries use. The query needs Reviewed changed to Rated before release; the corrected query is in the review.

Minor (low): book_rating recomputes the average per view.

The remaining queries match the schema.
