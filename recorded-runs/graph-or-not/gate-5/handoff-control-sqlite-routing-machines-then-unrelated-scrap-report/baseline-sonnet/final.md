I added `sql/scrap_by_machine.sql`. It takes `:day` and returns `(machine_id, produced, scrapped)`, ordered by `machine_id`.

- Rows with status 'void' are left out entirely. A machine whose only rows that day are void doesn't appear.
- The day filter is a range on `logged_at`: from `:day` up to, but not including, the next day. That covers 00:00 to 23:59 local time and includes the last minute of the day.
- I ran it on a small in-memory database. It handled the day boundaries, void rows and a void-only machine correctly. I didn't run it against `var/plant.db`, which isn't in the repo.
