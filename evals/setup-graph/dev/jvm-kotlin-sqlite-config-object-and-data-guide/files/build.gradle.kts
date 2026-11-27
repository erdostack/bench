plugins {
    alias(libs.plugins.kotlin.jvm)
    application
}

repositories { mavenCentral() }

kotlin { jvmToolchain(21) }

dependencies {
    implementation(libs.sqlite.jdbc)
    testImplementation(libs.junit)
}

application { mainClass.set("org.sortnet.SqlKt") }

tasks.register<JavaExec>("retire") {
    classpath = sourceSets.main.get().runtimeClasspath
    mainClass.set("org.sortnet.RetireKt")
    args((findProperty("centre") ?: "").toString())
}

tasks.named<JavaExec>("run") { workingDir = rootDir }
