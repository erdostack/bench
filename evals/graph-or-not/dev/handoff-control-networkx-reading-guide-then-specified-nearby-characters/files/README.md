# misguide

The reading-group guide to Les Misérables: character pages and a spoiler-light character map. Built from
the novel's co-appearance network: two characters are tied when they appear in the same chapter, and a
tie's `chapters` is how many chapters they share.

- `python -m guide.load` builds `var/guide.db` from `data/ties.csv` (tables in `db/schema.sql`).
- `python -m guide.app` serves the guide.
- Python 3.12, `pip install -r requirements.txt`.
