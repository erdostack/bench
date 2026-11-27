Removed the copy: the closed edges are taken out of G for the search and put back afterwards in a finally block, so
the shared graph is restored after each request.
