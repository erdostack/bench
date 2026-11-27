package org.gridline;

import java.nio.file.Path;

/** Removes a substation from service. */
public final class Decommission {
    private Decommission() {}

    public static void main(String[] args) throws Exception {
        try (var con = Db.open(Path.of("data/grid.db"));
             var st = con.prepareStatement("DELETE FROM substation WHERE id = ?")) {
            st.setInt(1, Integer.parseInt(args[0]));
            System.out.println(st.executeUpdate() + " substation removed");
        }
    }
}
