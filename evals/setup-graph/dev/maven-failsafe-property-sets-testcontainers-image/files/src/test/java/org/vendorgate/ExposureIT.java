package org.vendorgate;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.vendorgate.support.GraphContainer;

class ExposureIT {
    @Test
    void sharedSubTierFactoryReachesBothLines() throws Exception {
        try (var driver = GraphContainer.driver()) {
            assertEquals(List.of("Kettles", "Toasters"), new Exposure(driver).productLinesAtRisk("F-77"));
        }
    }
}
