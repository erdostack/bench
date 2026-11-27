# Model

    (:Piece {title, composer})
    (:Arrangement {arranger, year})-[:ARRANGEMENT_OF]->(:Piece | :Arrangement)
    (:Arrangement)-[:NEEDS]->(:Part {name})
    (:Concert {name, season})-[:INCLUDES]->(:Piece | :Arrangement)

A concert includes either the original piece or one of its arrangements; "has the choir sung this piece" has to
follow `ARRANGEMENT_OF` back.
