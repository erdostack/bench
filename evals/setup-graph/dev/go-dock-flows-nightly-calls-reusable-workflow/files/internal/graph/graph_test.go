package graph

import "testing"

func TestOpenDefaults(t *testing.T) {
	t.Setenv("NEO4J_URI", "")
	drv, err := Open()
	if err != nil || drv == nil {
		t.Fatalf("open: %v", err)
	}
}
