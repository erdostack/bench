package coop.parcelhub;

import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TrackingController {
    private final ParcelRepository parcels;

    public TrackingController(ParcelRepository parcels) {
        this.parcels = parcels;
    }

    @GetMapping("/track/{trackingNo}")
    public ResponseEntity<Map<String, Object>> track(@PathVariable String trackingNo) {
        return parcels.findByTrackingNo(trackingNo)
            .map(p -> ResponseEntity.ok(Map.<String, Object>of(
                "status", p.getStatus(), "hub", String.valueOf(p.getCurrentHub()), "updated", p.getUpdatedAt())))
            .orElse(ResponseEntity.notFound().build());
    }
}
