package main

import (
	"container/ring"
	"fmt"
	"strconv"
)

func printRing(r *ring.Ring) {
	n := r.Len()

	fmt.Print(" (", r.Value.(int), ")")
	r = r.Next()
	for i := 1; i < n; i++ {
		fmt.Print(" ", r.Value.(int))
		r = r.Next()
	}
	fmt.Println("")
}

func game(input []int, totalNodes, moveCount, resultCount int) {
	r := ring.New(totalNodes)
	index := make(map[int]*ring.Ring)

	min, max := 1024, -1
	minMax := func(v int) {
		if v < min {
			min = v
		}
		if v > max {
			max = v
		}
	}

	/* initialize the ring with our data */
	for i := 0; i < totalNodes; i++ {
		value := max + 1
		if i < len(input) {
			value = input[i]
		}
		minMax(value)
		r.Value = value
		index[value] = r
		r = r.Next()
	}

	for i := 0; i < moveCount; i++ {
		// fmt.Println("move: ", i+1)
		// printRing(r)

		removed := r.Unlink(3)
		// fmt.Print("pick up: ")
		// printRing(removed)

		/* find out the destination */
		currentNode := r
		currentLabel := r.Value.(int)
		candidate := currentLabel - 1

		/* take the first candidate that is not in the removed set */
		for {
			isInremoved := false
			removed.Do(func(v interface{}) {
				if v.(int) == candidate {
					isInremoved = true
				}
			})

			if !isInremoved {
				r = index[candidate]
				if r != nil {
					break
				}
			}

			candidate--
			if candidate < min {
				candidate = max
			}
		}

		// fmt.Println("destination:", r.Value.(int))
		// printRing(r)

		/* replace the removed elements */
		r.Link(removed)

		r = currentNode.Next()

		// fmt.Println("")
	}

	result := ""
	mulResult := 1
	for ; r.Value.(int) != 1; r = r.Next() {
	}
	for i, r := 0, r.Next(); i < resultCount; i, r = i+1, r.Next() {
		value := r.Value.(int)
		result += strconv.Itoa(value)
		mulResult *= value
	}

	fmt.Println("result: ", result, mulResult)
}

func main() {
	// input := []int{3, 8, 9, 1, 2, 5, 4, 6, 7} // test input
	input := []int{9, 7, 4, 6, 1, 8, 3, 5, 2}

	fmt.Print("part1 ")
	game(input, len(input), 100, 8)
	game(input, 1000000, 10000000, 2)
}
