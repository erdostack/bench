# fieldbook

The trials database of a plant-breeding programme: cultivars, the field trials they were grown in, the trial
sites and the people who ran them. LadybugDB, embedded in a small Flask API that the breeders' web pages
call. The database file is opened by the API process only.

    db/schema.cypher   table definitions
    api/catalog.py     which tables and relationships the API exposes, and how
    api/browse.py      the generic browse and lookup handlers
    api/routes.py      the Flask routes

About 5,200 cultivars, 1,900 trials, 60 sites, 140 people and 96,000 plantings (a cultivar grown in a
trial).
