Decision: need-more-information

It turns on one number nobody has yet: how many segments the regional extract holds. The worker has a hard 1.5 GB
limit; the prototype takes about 70 MB for the 38,000-segment county sample, so networkx in the worker fits up to
roughly ten to fifteen times the sample with room for Python itself. The national product (about 4 million
segments, over 100 times the sample) would not fit, and then the choice is between a graph database and a leaner
in-memory structure. At 300 checks a day with 2 s each, speed is not the issue; memory is. Please send the segment
count of the extract as soon as the supplier gives it. A graph database now would be a server bought before we
know we need it. Noted in docs/graph/DECISION.md.
