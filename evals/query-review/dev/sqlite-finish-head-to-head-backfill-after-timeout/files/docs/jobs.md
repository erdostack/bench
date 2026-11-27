# Jobs

- The scheduler runs each job at 01:00 with a connection to the club database and kills anything still
  running at 02:00. A killed job runs again the next night from the start, so a job must end up right
  however many times it was killed.
- At most 1,000 changed rows per transaction: the booking app shares the database.
