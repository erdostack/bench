# Jobs

- `run(conn)` gets a connection to `var/sbom.db` and returns a count for the log.
- The scanner and the image pages read all night: at most 2,000 changed rows per transaction.
- The scheduler kills any job still running at 03:00 and starts it again the next night. A job must end
  right when it is killed at any point and run again.
- `image_component` holds one row per (image, component): the scanner reports an image once per row, so
  a doubled row is a doubled finding.
- `image.component_count` is the number of distinct components in the image, i.e. its rows in
  `image_component`.
