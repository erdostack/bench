# Platform baseline

Every JVM service in the organisation applies the shared convention plugin (here: buildSrc). It sets the Java
toolchain and the minimum versions of shared clients, so a service cannot fall below them by accident.
