# The collection graph

    (:Object {accession, title, date_made, medium})
    (:Maker {name, born, died})            a person or a workshop
    (:Institution {code, name, city})
    (:Loan {id, starts, ends, purpose})

    (:Maker)-[:MADE {role}]->(:Object)
    (:Maker)-[:TRAINED_UNDER]->(:Maker)
    (:Object)-[:HELD_BY {from, to, how}]->(:Institution)     provenance, one relationship per period
    (:Object)-[:PART_OF]->(:Loan)-[:TO]->(:Institution)
    (:Loan)-[:FROM]->(:Institution)

`HELD_BY.to` is null for the current holder. A loan does not change `HELD_BY`.

The machine-written reference (labels, relationship types, property keys, constraints and indexes as the server
reports them) is `schema-2026-09.txt` in this directory. Regenerate it after a model change; do not edit it.
