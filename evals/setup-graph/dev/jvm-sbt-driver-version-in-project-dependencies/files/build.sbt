ThisBuild / scalaVersion := "3.3.6"
ThisBuild / organization := "org.bandgraph"

lazy val root = (project in file("."))
  .settings(
    name := "bandgraph",
    libraryDependencies ++= Seq(
      Dependencies.boltDriver,
      Dependencies.munit % Test
    ),
    Compile / run / fork := true
  )
