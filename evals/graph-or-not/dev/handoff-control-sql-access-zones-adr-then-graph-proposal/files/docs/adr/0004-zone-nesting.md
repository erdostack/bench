# ADR 0004: zone nesting in the door check

Status: Proposed (October 2026)
Author: Farid

## Context

Door controllers ask "may badge B open door D". A badge is granted zones. Zones nest: site, building, floor, room.
Today `access/door.py` compares the door's zone with the badge's zones exactly, so a grant on a building does not
open the rooms inside it and facilities grant every room by hand.

Measured in October 2026:

- 2,400 zones. The deepest nesting is 5.
- 35 door checks a second at shift change.
- Controllers give up after 100 ms.
- A recursive query that walks up from the door's zone took 4 ms on the staging copy.

## Options

A. Move zones into a graph database.
B. Load the zone tree into the access service's memory and walk it there.
C. Walk up the zone tree in Postgres with a recursive query.

## Outcome

Open.
