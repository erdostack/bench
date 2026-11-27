package org.ferryboard;

import java.time.Duration;

/** A sailing between two piers. Loaded from the operators' GTFS exports by a separate job. */
public record Timetable(String route, String fromPier, String toPier, Duration crossing) {}
