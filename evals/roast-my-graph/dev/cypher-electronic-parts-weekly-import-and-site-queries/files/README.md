# partsbin

Electronic component catalogue for a distributor price comparison site. Neo4j 5.26.

    import/schema.cypher    constraints and indexes
    import/weekly.cypher    weekly import, statements run in file order
    queries/site.cypher     the site's queries

The import reads the distributor feeds once a week: one row per offer (mpn, title, maker,
distributor, price, stock). Maker names are normalised to upper case before the import.

Sizes after the first full import: 310,000 parts from about 2,100 makers, 14 distributors,
1.2 million offers.

Site: the maker directory lists every maker with its number of parts; a maker page lists that maker's
parts; a part page lists its offers.
