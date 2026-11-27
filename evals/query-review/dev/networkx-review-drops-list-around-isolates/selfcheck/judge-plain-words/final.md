Left it as it is. The isolates call doesn't hand over a finished list, it looks through the network as it
goes, and the line deletes from that same network, so the job trips over itself and stops with an error
halfway. Making the list first is what avoids that. It's a short list anyway.
