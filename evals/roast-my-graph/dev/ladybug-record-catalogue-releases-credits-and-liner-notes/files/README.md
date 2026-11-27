# sleeve: record catalogue

LadybugDB, embedded, through the Python package (`ladybug==0.22.3`, see requirements.txt). One database
file, rebuilt from the editors' approved data and appended to by the import jobs.

- A release page shows the tracklist, the credits (who did what, linked to their pages) and, under
  "As printed", the credit lines exactly as they appear on the sleeve. Collectors use that section to tell
  pressings apart, so it is kept verbatim, typos and all.
- `load/parse_credits.py` reads the printed lines of new releases and writes *suggested* credits to a CSV;
  an editor approves them, and only approved rows become `CREDITED_ON` relationships.
- Person pages, "worked with" and label pages all come from relationships.

Big import next month: 1.4 million releases from a merged label archive.
