package org.hutnet

import java.io.File
import org.junit.jupiter.api.Assertions.assertTrue
import org.junit.jupiter.api.Test

class HutGraphTest {
    @Test
    fun everyHutHasATrail() {
        val g = HutGraph.load(File("../data"))
        assertTrue(g.vertexSet().all { g.degreeOf(it) > 0 })
    }
}
