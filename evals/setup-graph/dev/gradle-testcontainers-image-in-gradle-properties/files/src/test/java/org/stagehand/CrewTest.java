package org.stagehand;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

class CrewTest {
    @Test
    void onlyCertifiedPeopleRigTheBarn() throws Exception {
        try (var driver = GraphFixture.driver()) {
            assertEquals(List.of("Ines", "Tom"), new Crew(driver).riggersFor("The Barn"));
        }
    }
}
