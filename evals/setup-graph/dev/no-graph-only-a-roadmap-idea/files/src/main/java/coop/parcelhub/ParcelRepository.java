package coop.parcelhub;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ParcelRepository extends JpaRepository<Parcel, Long> {
    Optional<Parcel> findByTrackingNo(String trackingNo);
}
