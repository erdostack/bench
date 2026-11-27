# meeple-map

"If you liked that, try this" for a board-game café. Games, designers and mechanics sit in an embedded graph
database file next to the app, so the kiosk works without a network.

    npm ci
    npm run load            # builds ./var/meeple.kz from data/*.csv
    npm run kq -- queries/shared_mechanics.cypher

`npm run kq` opens the database read-only, runs the statement in the file and prints a table.
