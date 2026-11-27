package org.coldchain.it;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.coldchain.HandoffRepository;
import org.junit.jupiter.api.Test;

class HandoffIT {
    @Test
    void chainEndsAtTheClinic() throws Exception {
        var chain = new HandoffRepository(GraphFixture.driver()).chain("SH-2");
        assertEquals(1, chain.size());
    }
}
