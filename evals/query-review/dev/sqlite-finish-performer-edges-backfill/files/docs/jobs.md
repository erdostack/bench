# Jobs on prod

- A job commits at most 2,000 changed rows per transaction: the artist pages read `performed_on` while
  jobs run.
- A job that fails is run again the next night, unchanged, so a job must cope with being run again
  after stopping part-way.
