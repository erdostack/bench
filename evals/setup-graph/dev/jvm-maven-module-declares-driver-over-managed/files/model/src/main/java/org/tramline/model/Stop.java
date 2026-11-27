package org.tramline.model;

/** A tram stop as the loader reads it from the timetable export. */
public record Stop(String code, String name, double lat, double lon) {}
