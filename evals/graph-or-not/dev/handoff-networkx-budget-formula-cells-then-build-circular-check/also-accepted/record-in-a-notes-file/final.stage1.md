Decision: in-process-library. Noted in notes/circular-check.md.

The check is a cycle search over 14,000 cells and 31,000 references on every save; networkx did it in about 60 ms.
The hand-written check is the bug: it only pairs two cells on one sheet, so it finds 1 of the 5 loops. Finance's
rules go into the rewrite: loops anywhere count, self-references too, loops that stay on the Loan sheet are
intentional and are not flagged, and cells that only read a loop are not flagged. A graph database would be a
server in the save path of a spreadsheet editor.
