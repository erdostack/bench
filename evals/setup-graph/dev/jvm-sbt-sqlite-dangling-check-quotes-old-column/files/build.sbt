ThisBuild / scalaVersion := "3.3.6"

val sqliteJdbc = "3.49.1.0"

lazy val root = (project in file("."))
  .settings(
    name := "ferrylink",
    libraryDependencies += "org.xerial" % "sqlite-jdbc" % sqliteJdbc,
    Compile / run / fork := true
  )
