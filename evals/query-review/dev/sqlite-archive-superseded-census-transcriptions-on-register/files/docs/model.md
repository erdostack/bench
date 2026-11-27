# Model

`entity.kind`: `person`, `record` (one census household entry or parish register entry) or `volume` (the
register volume or census piece a record is in).

| relation kind | from | to | meaning |
|---|---|---|---|
| `appears_in` | person | record | a volunteer's transcription: this person is named in this record |
| `parent_of` | person | person | a family link a volunteer has proposed from the records |
| `in_volume` | record | volume | where the record is |

`status`: `current`; `superseded` (a corrected transcription replaced it; kept only for the audit trail);
`disputed` (two volunteers disagree and a checker has not decided yet; shown in search with a warning).
