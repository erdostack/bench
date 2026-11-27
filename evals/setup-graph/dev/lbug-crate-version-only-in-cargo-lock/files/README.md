# tunebook

A session musician's notebook: traditional tunes, the sets they get played in, and which tune usually follows
which. Built to answer "what do people play after The Silver Spear?" without scrolling through a phone.

The tunes live in an embedded graph database (LadybugDB, through the `lbug` crate). It is a directory under
`var/`; nothing runs in the background.

    just load                                  # build var/tunebook.lbug from data/
    just q queries/what_follows.cypher        # run a saved query, read-only

Both recipes are thin wrappers around the two binaries in `src/bin/`.
