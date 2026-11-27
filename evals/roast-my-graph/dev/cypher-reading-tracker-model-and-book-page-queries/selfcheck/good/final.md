The main model change: Rating should be a relationship, not a node. It only ever links one reader
to one book and carries stars and a date, so it costs you an extra hop on every rating query,
including the book page's also-loved list. Make it RATED {stars, rated_at} from Reader to Book.
Details in docs/graph/ROAST.md and findings.json.
