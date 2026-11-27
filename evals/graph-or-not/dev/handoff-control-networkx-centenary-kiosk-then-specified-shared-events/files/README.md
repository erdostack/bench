# centenary-kiosk

Touch-screen kiosk for the department's centenary exhibit on the Southern Women study (Davis, Gardner and
Gardner): eighteen women and the fourteen social events they were recorded attending. Runs on a Raspberry
Pi in the foyer.

- `python -m kiosk.load` builds `var/kiosk.db` from `data/` (tables in `db/schema.sql`).
- `python -m kiosk.app` serves the screens on localhost.
- Python 3.11 (the Pi's), networkx is installed there.
