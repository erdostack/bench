# Catalogue model (the part we use)

    (:Work {title, first_published})-[:HAS_EDITION]->(:Edition {isbn, year, language})
    (:Work)-[:ABOUT]->(:Subject {label})
    (:Subject)-[:BROADER]->(:Subject)        narrower points at broader

The cataloguing team has more labels than this (holdings, branches, loans). We do not query them.
