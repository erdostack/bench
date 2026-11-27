package org.countybus.web;

import io.javalin.Javalin;

public final class App {
    public static void main(String[] args) {
        Javalin.create().get("/health", ctx -> ctx.result("ok")).start(7070);
    }
}
