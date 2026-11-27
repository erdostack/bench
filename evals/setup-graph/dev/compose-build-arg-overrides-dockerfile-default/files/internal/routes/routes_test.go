package routes

import (
	"reflect"
	"testing"
)

func TestOrderVisitsNearestFirst(t *testing.T) {
	position := map[string]int{"A1": 0, "A4": 3, "A2": 1, "A9": 8}
	distance := func(a, b string) int {
		d := position[a] - position[b]
		if d < 0 {
			return -d
		}
		return d
	}
	got := Order("A1", distance, []string{"A9", "A2", "A4"})
	if want := []string{"A2", "A4", "A9"}; !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v, want %v", got, want)
	}
}
