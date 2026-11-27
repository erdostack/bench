Decision: in-process-library

Not Neo4j. The data is 18 women, 14 events and 89 attendances. It is in a CSV file and will never change, and the pages get a few dozen visitors a week on a small shared host. A graph database server would be far more than this needs. It would be another service to install and keep running, and a shared host probably can't run it at all. Recursive SQL doesn't apply either, because there is no SQL database here, only the CSV.

"Circles" is a real graph walk: ring by ring outward from one woman. So I used the graph library the project already depends on (`networkx` is in `requirements.txt`, and `setup.py` already builds the CSV from its bundled copy of the study). The whole list loads into memory on each page view in well under a millisecond.

The TODO in `society/pages.py` is done as `circles_page(name)`. It returns the name and a list of rings:
- Ring 1 is every woman who attended at least one event with her.
- Ring 2 is every woman who shared an event with someone in ring 1, and so on, out to the whole network.
- Each woman appears once, in her nearest ring, and the names within a ring are sorted.
- An unknown name raises `KeyError`.

I tried it for all 18 women. Each reaches the other 17, so the network is fully connected. For Brenda Rogers, 15 women are in ring 1 and 2 are in ring 2.

I only wrote the data function, since `pages.py` is rendering-only in this repo and there's no template or web route to hook into. You'll need to wire `circles_page` into the page and add the woman picker, which can reuse `index_page()["women"]`. I added no test files and no new dependencies.
