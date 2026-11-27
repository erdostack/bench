package coop.parcelhub;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import java.time.Instant;

@Entity
public class Parcel {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "tracking_no", nullable = false, unique = true)
    private String trackingNo;

    private String recipient;
    private String status;

    @Column(name = "current_hub")
    private String currentHub;

    @Column(name = "updated_at")
    private Instant updatedAt;

    public String getTrackingNo() { return trackingNo; }
    public String getStatus() { return status; }
    public String getCurrentHub() { return currentHub; }
    public Instant getUpdatedAt() { return updatedAt; }
}
