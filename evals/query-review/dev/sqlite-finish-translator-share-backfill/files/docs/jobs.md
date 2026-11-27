# Jobs

Jobs run from the scheduler. When a job fails, the scheduler (or whoever is on call) runs it again
from the start with the same command, so every job must be safe to run again over its own partial work.
