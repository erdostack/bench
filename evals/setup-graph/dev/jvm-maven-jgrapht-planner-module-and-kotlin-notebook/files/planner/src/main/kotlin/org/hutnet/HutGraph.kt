package org.hutnet

import java.io.File
import org.jgrapht.graph.DefaultWeightedEdge
import org.jgrapht.graph.SimpleDirectedWeightedGraph

typealias Trails = SimpleDirectedWeightedGraph<String, DefaultWeightedEdge>

object HutGraph {
    fun load(dataDir: File): Trails {
        val g = Trails(DefaultWeightedEdge::class.java)
        File(dataDir, "huts.csv").readLines().drop(1).forEach { g.addVertex(it.substringBefore(',')) }
        File(dataDir, "trails.csv").readLines().drop(1).forEach { line ->
            val (from, to, hours) = line.split(',')
            g.setEdgeWeight(g.addEdge(from, to), hours.toDouble())
        }
        return g
    }
}
