package org.ridgeway;

import java.sql.SQLException;

/** Applies a re-survey: removes junctions that no longer exist on the ground. */
public final class Survey {
    private Survey() {}

    public static void removeJunction(int id) throws SQLException {
        try (var con = Trails.open(); var st = con.prepareStatement("DELETE FROM junction WHERE id = ?")) {
            st.setInt(1, id);
            st.executeUpdate();
        }
    }
}
