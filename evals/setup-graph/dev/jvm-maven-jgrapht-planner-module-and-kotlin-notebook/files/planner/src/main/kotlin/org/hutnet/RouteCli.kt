package org.hutnet

import java.io.File
import org.jgrapht.alg.shortestpath.DijkstraShortestPath
import org.jgrapht.alg.shortestpath.YenKShortestPath

fun main(args: Array<String>) {
    require(args.size >= 2) { "usage: bin/route <from-hut> <to-hut> [k]" }
    val g = HutGraph.load(File("data"))
    val k = args.getOrNull(2)?.toInt() ?: 1
    if (k == 1) {
        val path = DijkstraShortestPath(g).getPath(args[0], args[1]) ?: error("no route")
        println("${path.vertexList.joinToString(" -> ")}  (${path.weight} h)")
    } else {
        YenKShortestPath(g).getPaths(args[0], args[1], k).forEach { p ->
            println("${p.vertexList.joinToString(" -> ")}  (${p.weight} h)")
        }
    }
}
