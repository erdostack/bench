package org.citeweave;

/** Rebuilds the store from the corpus files: one :Paper node per line, a :CITES relationship per reference. */
public final class Load {
    private Load() {}

    public static void main(String[] args) throws Exception {
        Loader.rebuild(java.nio.file.Path.of(args[0]), java.nio.file.Path.of(args[1]));
    }
}
