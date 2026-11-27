Took out the copy, but not the way the comment suggests: everyone shares one road graph (network() hands out the same
object to every request), so deleting closed roads from it would keep them closed for the next person too. I now look
at the graph through a filter that hides just this request's closed roads, so nothing is copied and nothing is
changed for anyone else. Same answers as before.
