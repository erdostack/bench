# Model

`nodes(id, kind, ref, term, lang)`: `kind` is `course`, `language` or `teacher`. Language refs are codes
(`ES`, `FR`, ...). Courses have a `term` (`2026-autumn`, `2027-spring`, ...) and a `lang`, the code of the
language taught; conversation clubs mix languages and have `lang` NULL.

| edge kind | src | dst |
|---|---|---|
| `in_language` | course | language (the node whose `ref` is the course's `lang`) |
| `taught_by` | course | teacher |

A course has at most one `in_language` edge.
