# Model

`nodes.kind` is `donor` (code `D-200417`) or `centre` (code `DC-07`).

| edge kind | src | dst | `day` |
|---|---|---|---|
| `donated_at` | donor | centre | the day of the donation (one edge per donation; a donor gives at most once a day) |
| `home_centre` | donor | centre | the day of the donation the home centre was taken from |

**Home centre.** An active donor who has given at least once has exactly one `home_centre`: the centre
of their most recent donation, with that donation's day. Withdrawn donors and donors who have never
given have none. Donor care may set a donor's `home_centre` by hand (when someone moves house); a
`home_centre` that exists is never changed by a script. The booking app has set it for new donations
since September 2026, so older donors may still lack one.
