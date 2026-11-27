# Operating notes

## Starting and stopping

`make up` and `make down`. The stack settings (image tag, heap, ports) are in `config/stack.env`; change them
there, not in `docker-compose.yml`, whose values are only fallbacks for people running compose by hand.

## Reloading the timetable

`make load` wipes the graph and loads `data/`. It is the only thing that writes. The harbour office sends new
CSVs twice a year.

## Backups

None. The graph can always be rebuilt from `data/`.
